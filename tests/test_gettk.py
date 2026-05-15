"""
gettk模块的单元测试

该测试模块用于验证tk令牌生成函数的正确性，包括：
- 基本文本的tk生成
- 特殊字符和Unicode文本的处理
- 空字符串和边界条件
- tk格式的正确性
"""
import pytest
from gettk import get_tk, _TKK, _RL, _TL


class TestTKK:
    """测试_TKK函数"""

    def test_tkk_returns_list(self):
        """验证_TKK返回一个包含两个整数的列表"""
        result = _TKK()
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(x, int) for x in result)

    def test_tkk_values_are_consistent(self):
        """验证_TKK返回值的一致性"""
        result1 = _TKK()
        result2 = _TKK()
        assert result1 == result2


class TestRL:
    """测试_RL辅助函数"""

    def test_rl_with_plus_operator(self):
        """测试使用+运算符的_RL函数"""
        result = _RL(100, "+-a^+6")
        assert isinstance(result, int)

    def test_rl_with_minus_operator(self):
        """测试使用-运算符的_RL函数"""
        result = _RL(100, "+-3^+b+-f")
        assert isinstance(result, int)

    def test_rl_returns_integer(self):
        """验证_RL始终返回整数"""
        result = _RL(1000, "+-a^+6")
        assert isinstance(result, int)


class TestTL:
    """测试_TL函数（tk生成的核心逻辑）"""

    def test_tl_returns_string(self):
        """验证_TL返回字符串格式的tk值"""
        result = _TL("hello")
        assert isinstance(result, str)

    def test_tl_format(self):
        """验证tk值的格式为'数字.数字'"""
        result = _TL("test")
        parts = result.split(".")
        assert len(parts) == 2
        assert parts[0].isdigit()
        assert parts[1].isdigit()

    def test_tl_different_inputs(self):
        """验证不同输入产生不同的tk值"""
        tk1 = _TL("hello")
        tk2 = _TL("world")
        assert tk1 != tk2

    def test_tl_same_input_consistent(self):
        """验证相同输入产生相同的tk值"""
        tk1 = _TL("test")
        tk2 = _TL("test")
        assert tk1 == tk2


class TestGetTk:
    """测试get_tk公共接口函数"""

    def test_get_tk_basic_text(self):
        """测试基本英文文本的tk生成"""
        tk = get_tk("hello")
        assert isinstance(tk, str)
        assert "." in tk

    def test_get_tk_chinese_text(self):
        """测试中文文本的tk生成"""
        tk = get_tk("你好世界")
        assert isinstance(tk, str)
        assert "." in tk

    def test_get_tk_mixed_language(self):
        """测试混合语言文本的tk生成"""
        tk = get_tk("hello 你好")
        assert isinstance(tk, str)
        assert "." in tk

    def test_get_tk_empty_string(self):
        """测试空字符串的tk生成"""
        tk = get_tk("")
        assert isinstance(tk, str)
        assert "." in tk

    def test_get_tk_special_characters(self):
        """测试包含特殊字符的文本"""
        tk = get_tk("hello@world#123")
        assert isinstance(tk, str)
        assert "." in tk

    def test_get_tk_numbers_only(self):
        """测试纯数字文本"""
        tk = get_tk("12345")
        assert isinstance(tk, str)
        assert "." in tk

    def test_get_tk_unicode_characters(self):
        """测试Unicode字符（emoji等）"""
        tk = get_tk("Hello 🌍 World")
        assert isinstance(tk, str)
        assert "." in tk

    def test_get_tk_long_text(self):
        """测试长文本的tk生成"""
        long_text = "a" * 1000
        tk = get_tk(long_text)
        assert isinstance(tk, str)
        assert "." in tk

    def test_get_tk_newlines_and_spaces(self):
        """测试包含换行符和空格的文本"""
        tk = get_tk("hello\nworld\ttest")
        assert isinstance(tk, str)
        assert "." in tk

    def test_get_tk_consistency(self):
        """验证相同文本多次调用生成相同的tk"""
        text = "consistency test"
        tokens = [get_tk(text) for _ in range(5)]
        assert len(set(tokens)) == 1
