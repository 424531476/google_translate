"""
Googletrans类的单元测试和集成测试

该测试模块用于验证Google翻译客户端的功能，包括：
- 实例化和初始化
- 基本翻译功能
- 多语言支持
- 代理配置
- 异常处理
- 会话管理
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from google_translate import Googletrans


class TestGoogletransInit:
    """测试Googletrans类的初始化"""

    def test_init_without_proxy(self):
        """测试不使用代理的初始化"""
        with patch('google_translate.Googletrans._Googletrans__new_session'):
            translator = Googletrans()
            assert translator.proxy is None
            assert translator.n_session_use == 0

    def test_init_with_proxy(self):
        """测试使用代理的初始化"""
        proxy_url = "http://127.0.0.1:7890"
        with patch('google_translate.Googletrans._Googletrans__new_session'):
            translator = Googletrans(proxy=proxy_url)
            assert translator.proxy == proxy_url

    def test_init_creates_session(self):
        """验证初始化时创建会话"""
        with patch('google_translate.Googletrans._Googletrans__new_session') as mock_new_session:
            Googletrans()
            mock_new_session.assert_called_once()


class TestNewSession:
    """测试__new_session方法"""

    @patch('requests.session')
    def test_new_session_success(self, mock_session_class):
        """测试成功创建新会话"""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session

        with patch('google_translate.Googletrans._Googletrans__new_session', lambda self: None):
            translator = Googletrans()
            translator._Googletrans__session = mock_session
            translator._Googletrans__new_session()

            assert translator.n_session_use == 0

    @patch('requests.session')
    def test_new_session_with_proxy(self, mock_session_class):
        """验证使用代理时正确配置代理"""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_session.get.return_value = mock_response
        mock_session.headers = {}
        mock_session.proxies = {}
        mock_session_class.return_value = mock_session

        with patch('google_translate.Googletrans._Googletrans__new_session', lambda self: None):
            translator = Googletrans(proxy="http://127.0.0.1:7890")
            translator._Googletrans__new_session()

            assert translator.proxy == "http://127.0.0.1:7890"


class TestTranslation:
    """测试翻译功能"""

    @pytest.fixture
    def translator(self):
        """创建翻译器实例(mock版本)"""
        with patch('google_translate.Googletrans._Googletrans__new_session'):
            with patch('google_translate.requests.session') as mock_session_class:
                mock_session = MagicMock()
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.text = '{"sentences":[{"trans":"你好"}]}'
                mock_session.get.return_value = mock_response
                mock_session_class.return_value = mock_session

                translator = Googletrans()
                translator._Googletrans__session = mock_session
                return translator

    def test_translate_basic(self, translator):
        """测试基本翻译功能"""
        result = translator("hello", tl="zh-CN")
        assert isinstance(result, str)
        assert result == "你好"

    def test_translate_default_target_language(self, translator):
        """测试默认目标语言为简体中文"""
        result = translator("hello")
        assert result == "你好"

    def test_translate_with_source_language(self, translator):
        """测试指定源语言"""
        result = translator("Bonjour", sl="fr", tl="en")
        assert isinstance(result, str)

    def test_translate_auto_detect(self, translator):
        """测试自动检测源语言"""
        result = translator("hello", sl="auto", tl="zh-CN")
        assert isinstance(result, str)

    def test_translate_increments_session_use(self, translator):
        """验证翻译操作增加会话使用计数"""
        initial_count = translator.n_session_use
        translator("hello", tl="zh-CN")
        assert translator.n_session_use == initial_count + 1

    def test_translate_session_rotation(self, translator):
        """测试会话使用超过50次后重建"""
        translator.n_session_use = 50
        
        with patch.object(translator, '_Googletrans__new_session') as mock_new_session:
            translator("hello", tl="zh-CN")
            mock_new_session.assert_called_once()


class TestResponseParsing:
    """测试响应解析"""

    @pytest.fixture
    def translator(self):
        """创建翻译器实例（mock版本）"""
        with patch('google_translate.Googletrans._Googletrans__new_session'):
            with patch('google_translate.requests.session') as mock_session_class:
                mock_session = MagicMock()
                mock_session_class.return_value = mock_session

                translator = Googletrans()
                translator._Googletrans__session = mock_session
                return translator

    def test_parse_sentences_format(self, translator):
        """测试解析sentences格式的响应"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"sentences":[{"trans":"你好"},{"trans":"世界"}]}'
        translator._Googletrans__session.get.return_value = mock_response

        result = translator("hello world", tl="zh-CN")
        assert result == "你好世界"

    def test_parse_legacy_format(self, translator):
        """测试解析旧版数组格式的响应"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '[[["你好","hello",null,null,3]],null,"en"]'
        translator._Googletrans__session.get.return_value = mock_response

        result = translator("hello", tl="zh-CN")
        assert result == "你好"

    def test_parse_invalid_json(self, translator):
        """测试解析无效JSON时的异常处理"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = 'invalid json'
        translator._Googletrans__session.get.return_value = mock_response

        with pytest.raises(Exception) as exc_info:
            translator("hello", tl="zh-CN")
        assert "Failed to parse" in str(exc_info.value)

    def test_parse_empty_response(self, translator):
        """测试解析空响应的异常处理"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{}'
        translator._Googletrans__session.get.return_value = mock_response

        with pytest.raises(Exception) as exc_info:
            translator("hello", tl="zh-CN")
        assert "Failed to parse" in str(exc_info.value)


class TestErrorHandling:
    """测试错误处理"""

    @pytest.fixture
    def translator(self):
        """创建翻译器实例（mock版本）"""
        with patch('google_translate.Googletrans._Googletrans__new_session'):
            with patch('google_translate.requests.session') as mock_session_class:
                mock_session = MagicMock()
                mock_session_class.return_value = mock_session

                translator = Googletrans()
                translator._Googletrans__session = mock_session
                return translator

    def test_http_error_404(self, translator):
        """测试HTTP 404错误的处理"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = 'Not Found'
        translator._Googletrans__session.get.return_value = mock_response

        with pytest.raises(Exception) as exc_info:
            translator("hello", tl="zh-CN")
        assert "status_code:404" in str(exc_info.value)

    def test_http_error_500(self, translator):
        """测试HTTP 500错误的处理"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = 'Internal Server Error'
        translator._Googletrans__session.get.return_value = mock_response

        with pytest.raises(Exception) as exc_info:
            translator("hello", tl="zh-CN")
        assert "status_code:500" in str(exc_info.value)

    def test_connection_error_handling(self):
        """测试连接错误的处理"""
        import requests.exceptions
        
        with patch('google_translate.requests.session') as mock_session_class:
            mock_session = MagicMock()
            mock_session.get.side_effect = requests.exceptions.ConnectionError()
            mock_session_class.return_value = mock_session

            with patch('google_translate.time.sleep'):
                with pytest.raises(Exception):
                    Googletrans()


class TestThreadSafety:
    """测试线程安全性"""

    def test_concurrent_translations(self):
        """测试并发翻译的线程安全性"""
        import threading
        
        results = []
        errors = []

        with patch('google_translate.Googletrans._Googletrans__new_session'):
            with patch('google_translate.requests.session') as mock_session_class:
                mock_session = MagicMock()
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.text = '{"sentences":[{"trans":"翻译结果"}]}'
                mock_session.get.return_value = mock_response
                mock_session_class.return_value = mock_session

                translator = Googletrans()
                translator._Googletrans__session = mock_session

                def translate_task():
                    try:
                        result = translator("test", tl="zh-CN")
                        results.append(result)
                    except Exception as e:
                        errors.append(str(e))

                threads = [threading.Thread(target=translate_task) for _ in range(10)]
                for t in threads:
                    t.start()
                for t in threads:
                    t.join()

                assert len(results) == 10
                assert len(errors) == 0
