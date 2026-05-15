import requests
import json
import time
import threading
from urllib import parse
from gettk import get_tk


class Googletrans:
    def __init__(self):
        self.lock = threading.RLock()
        self.__session = requests.session()
        self.n_session_use = 0
        self.__new_session()

    def __new_session(self) -> None:
        """
        创建新的会话并获取有效的Cookies

        该方法会尝试最多3次建立新的会话连接，每次都会：
        1. 创建新的requests session对象
        2. 设置User-Agent和Referer请求头
        3. 访问Google翻译主页以获取Cookies
        4. 如果成功则更新实例的session并重置使用计数

        :return: None
        :raises Exception: 当3次尝试都失败时抛出最后一次捕获的异常
        """
        # 最多重试3次以建立新会话
        for i in range(3):
            user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
            referer = "https://translate.google.cn/"
            session = requests.session()
            session.headers["User-Agent"] = user_agent
            session.headers["referer"] = referer

            # 尝试访问Google翻译页面以获取Cookies
            try:
                response = session.get(r"https://translate.google.cn")
            except requests.exceptions.ConnectionError as e:
                time.sleep(0.5)
                continue

            # 检查响应状态码是否为200
            if response.status_code != 200:
                e = Exception("status_code:%d" % response.status_code)
                continue

            # 线程安全地更新会话对象和使用计数
            self.lock.acquire()
            self.__session = session
            self.n_session_use = 0
            self.lock.release()
            return

        # 3次尝试均失败，抛出异常
        raise e

    def __call__(self, q: str, sl: str = "auto", tl: str = "zh-CN", **kwargs) -> str:
        """
        执行文本翻译操作

        该方法通过调用Google Translate API实现文本翻译功能。它会自动管理HTTP会话，
        在会话使用超过50次后自动创建新会话以避免被限制。支持多种响应格式的解析。

        :param q: 需要翻译的文本内容
        :param sl: 源语言代码，默认为"auto"表示自动检测语言
        :param tl: 目标语言代码，默认为"zh-CN"（简体中文）
        :param kwargs: 传递给requests.get()方法的额外参数，如timeout、proxies等
        :return: 翻译后的文本字符串
        :raises Exception: 当HTTP请求失败或响应解析异常时抛出异常
        """
        # 初始化客户端标识并生成翻译token
        client = "gtx"
        tk = get_tk(q)

        # 线程安全地管理session生命周期，超过使用阈值则重建session
        self.lock.acquire()
        if self.n_session_use >= 50:
            self.__new_session()
        self.n_session_use += 1
        session = self.__session
        self.lock.release()

        # 构建包含所有必要参数的Google Translate API请求URL
        url_format = (
            r"https://translate.googleapis.com/translate_a/single?"
            "client={client}&sl={sl}&tl={tl}&hl=zh-CN&dt=t&dt=bd&dj=1&source=icon&tk={tk}&q={q}"
        )
        url = url_format.format(client=client, q=parse.quote(q), tk=tk, sl=sl, tl=tl)

        # 发送GET请求获取翻译结果并验证HTTP响应状态
        response = session.get(url, **kwargs)
        if response.status_code != 200:
            raise Exception("status_code:%s" % response.status_code, response.text)

        # 解析JSON响应数据，兼容新旧两种API响应格式并提取翻译文本
        try:
            data = json.loads(response.text)
            if "sentences" in data:
                return "".join([sentence["trans"] for sentence in data["sentences"]])
            else:
                text_list = data[0]
                return "".join([text[0] for text in text_list])
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            raise Exception("Failed to parse translation response: %s" % str(e))


if __name__ == "__main__":
    translate = Googletrans()
    print(translate("hello", tl="zh-CN"))
