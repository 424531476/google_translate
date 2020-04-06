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
        '''
        更换新的Cookies
        :return:
        '''
        for i in range(3):
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
            referer = 'https://translate.google.cn/'
            session = requests.session()
            session.headers['User-Agent'] = user_agent
            session.headers['referer'] = referer
            try:
                response = session.get(r'https://translate.google.cn')
            except requests.exceptions.ConnectionError as e:
                time.sleep(0.5)
                continue
            if response.status_code != 200:
                e = Exception('status_code:%d' % response.status_code)
                continue
            self.lock.acquire()
            self.__session = session
            self.n_session_use = 0
            self.lock.release()
            return
        raise e

    def __call__(self, q: str, sl: str = 'auto', tl: str = 'zh-CN', **kwargs) -> str:
        '''
        调用翻译
        :param q: 需要翻译的文本
        :param sl: 参数q的语言代码默认自动检测
        :param tl: 目标语言的语言代码
        :param kwargs: 传给requests的参数
        :return: 返回翻译结果
        '''
        client = 'webapp'
        tk = get_tk(q)
        self.lock.acquire()
        if self.n_session_use >= 50:
            self.__new_session()
        self.n_session_use += 1
        session = self.__session
        self.lock.release()
        url_format = r'https://translate.google.cn/translate_a/single?' \
                     'client={client}&sl={sl}&tl={tl}&dt=t&q={q}&tk={tk}'
        url = url_format.format(client=client, q=parse.quote(q), tk=tk, sl=sl, tl=tl)
        response = session.get(url, **kwargs)
        if response.status_code != 200:
            raise Exception('status_code:%s' % response.status_code, response.text)
        text_list = json.loads(response.text)[0]
        return ''.join([text[0] for text in text_list])


if __name__ == '__main__':
    translate = Googletrans()
    print(translate('hello', tl='zh-CN'))
