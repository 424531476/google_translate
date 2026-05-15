"""
Pytest配置文件

该文件用于配置pytest的行为，包括：
- 定义自定义标记（markers）
- 提供共享的fixture
- 配置测试收集规则
"""
import pytest


def pytest_configure(config):
    """
    配置pytest的自定义标记

    定义以下标记：
    - integration: 标记需要网络连接的集成测试
    - slow: 标记执行时间较长的测试
    """
    config.addinivalue_line(
        "markers", "integration: mark test as requiring network connection"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


@pytest.fixture
def sample_texts():
    """
    提供常用的测试文本样本

    :return: 包含多种语言文本的字典
    """
    return {
        "english": "hello world",
        "chinese": "你好世界",
        "japanese": "こんにちは世界",
        "french": "Bonjour le monde",
        "spanish": "Hola mundo",
        "german": "Hallo Welt",
        "empty": "",
        "special_chars": "Hello @ World # 123",
        "unicode": "Hello 🌍 World 🚀",
        "long_text": "Python is a high-level programming language that emphasizes code readability.",
    }


@pytest.fixture
def target_languages():
    """
    提供常用的目标语言代码列表

    :return: 常见语言代码列表
    """
    return ["zh-CN", "en", "ja", "fr", "es", "de", "ko", "ru"]
