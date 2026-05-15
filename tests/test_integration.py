"""
Google翻译的集成测试

该测试模块用于验证实际的翻译功能，需要网络连接。
这些测试可能会因为网络问题或Google服务变更而失败。

注意：运行这些测试前请确保网络连接正常，并遵守使用限制。
"""
import pytest
from google_translate import Googletrans


@pytest.mark.integration
class TestIntegrationTranslation:
    """集成测试：实际调用Google翻译API"""

    @pytest.fixture(scope="module")
    def translator(self):
        """创建翻译器实例，在整个测试模块中复用"""
        return Googletrans()

    def test_english_to_chinese(self, translator):
        """测试英文到中文的翻译"""
        result = translator("hello", tl="zh-CN")
        assert isinstance(result, str)
        assert len(result) > 0
        assert "你好" in result or "您好" in result

    def test_chinese_to_english(self, translator):
        """测试中文到英文的翻译"""
        result = translator("你好", sl="zh-CN", tl="en")
        assert isinstance(result, str)
        assert len(result) > 0
        assert "hello" in result.lower() or "hi" in result.lower()

    def test_auto_detect_language(self, translator):
        """测试自动语言检测"""
        result = translator("Bonjour", tl="en")
        assert isinstance(result, str)
        assert len(result) > 0
        assert "hello" in result.lower() or "good day" in result.lower()

    def test_japanese_to_chinese(self, translator):
        """测试日文到中文的翻译"""
        result = translator("こんにちは", sl="ja", tl="zh-CN")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_spanish_to_english(self, translator):
        """测试西班牙文到英文的翻译"""
        result = translator("Hola", sl="es", tl="en")
        assert isinstance(result, str)
        assert len(result) > 0
        assert "hello" in result.lower() or "hi" in result.lower()

    def test_long_text_translation(self, translator):
        """测试长文本翻译"""
        text = "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation."
        result = translator(text, tl="zh-CN")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_special_characters(self, translator):
        """测试包含特殊字符的文本翻译"""
        result = translator("Hello, World! @#$%", tl="zh-CN")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_numbers_and_symbols(self, translator):
        """测试数字和符号的翻译"""
        result = translator("123 + 456 = 579", tl="zh-CN")
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.slow
    def test_multiple_translations(self, translator):
        """测试多次连续翻译（验证会话管理）"""
        texts = ["hello", "world", "python", "programming", "test"]
        results = []
        
        for text in texts:
            result = translator(text, tl="zh-CN")
            assert isinstance(result, str)
            assert len(result) > 0
            results.append(result)
        
        assert len(results) == 5

    def test_unicode_characters(self, translator):
        """测试Unicode字符（emoji等）的翻译"""
        result = translator("Hello 🌍 World 🚀", tl="zh-CN")
        assert isinstance(result, str)
        assert len(result) > 0


@pytest.mark.integration
class TestSessionManagement:
    """测试会话管理机制"""

    def test_session_reuse(self):
        """测试会话重用机制"""
        translator = Googletrans()
        
        initial_session = translator._Googletrans__session
        initial_use_count = translator.n_session_use
        
        translator("hello", tl="zh-CN")
        
        assert translator.n_session_use == initial_use_count + 1
        assert translator._Googletrans__session is initial_session

    def test_session_rotation_after_threshold(self):
        """测试达到阈值后的会话轮换"""
        translator = Googletrans()
        
        translator.n_session_use = 50
        old_session = translator._Googletrans__session
        
        translator("hello", tl="zh-CN")
        
        new_session = translator._Googletrans__session
        assert new_session is not old_session
        assert translator.n_session_use == 1
