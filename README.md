**一个免费的Google翻译Python接口库，通过直接调用Google翻译网页版服务实现文本翻译功能**

---

## 📋 目录

- [项目简介](#-项目简介)
- [核心特性](#-核心特性)
- [安装指南](#-安装指南)
- [快速开始](#-快速开始)
- [API文档](#-api文档)
- [支持的语言](#-支持的语言)
- [测试](#-测试)

---

## 🌟 项目简介

本项目提供了一个简单易用的Google翻译API封装，绕过官方API的成本和配额限制。它自动处理反爬机制（如tk参数生成、cookies管理），支持多种语言互译，适合需要批量翻译或自动化翻译的场景。

### 为什么选择本项目？

- 💰 **完全免费**：无需API密钥，无使用配额限制
- 🚀 **开箱即用**：简洁的API设计，几行代码即可实现翻译功能
- 🔒 **智能防护**：自动处理反爬机制，降低IP封禁风险
- 🌍 **多语言支持**：支持超过100种语言的互译
- ⚡ **高性能**：会话复用机制，减少连接开销

---

## ✨ 核心特性

- ✅ **完全免费**：无需API密钥，无使用配额限制
- ✅ **自动计算tk值**：内置tk令牌生成算法，自动处理Google翻译的动态验证
- ✅ **智能会话管理**：自动更换cookies避免IP封禁，每50次请求自动重建会话
- ✅ **多线程安全**：使用线程锁保证并发访问的安全性
- ✅ **自动语言检测**：支持源语言自动识别
- ✅ **代理支持**：可配置HTTP/HTTPS代理，增强访问灵活性
- ✅ **广泛的语言支持**：支持超过100种语言的互译
- ✅ **响应格式兼容**：同时支持新旧两种Google翻译API响应格式
- ✅ **错误处理完善**：提供详细的异常信息和错误提示

---

## 📦 安装指南

### 系统要求

- **Python 3.10+**（代码使用了Python 3.10的联合类型注解语法 `str | None`）
- uv包管理器（推荐，需要Python 3.8+）
- 网络连接（可访问Google翻译服务）

### 使用uv安装

```
# Google Translate API

一个免费的Google翻译Python接口库，通过直接调用Google翻译网页版服务实现文本翻译功能。

## 特性

- 💰 完全免费，无需API密钥
- 🚀 开箱即用，简洁的API设计
- 🔒 自动处理反爬机制（tk参数、cookies管理）
- 🌍 支持100+种语言互译
- ⚡ 会话复用，高性能

## 安装与使用

```bash
# 运行项目
uv run python -c "from google_translate import Googletrans; translate = Googletrans(); print(translate('hello', tl='zh-CN'))"
```

## 快速开始

### 基本用法

```python
from google_translate import Googletrans

# 创建翻译实例
translate = Googletrans()

# 翻译文本（默认翻译为简体中文）
result = translate('hello', tl='zh-CN')
print(result)  # 输出: 你好

# 指定源语言和目标语言
result = translate('Bonjour', sl='fr', tl='en')
print(result)  # 输出: Hello
```

### 使用代理

```python
from google_translate import Googletrans

# 配置代理服务器
translate = Googletrans(proxy="http://127.0.0.1:7890")
result = translate('hello world', tl='zh-CN')
print(result)
```

## API文档

### Googletrans类

**初始化：**
```python
Googletrans(proxy: str | None = None)
```
- `proxy`: 代理服务器地址，如 `"http://host:port"`

**翻译方法：**
```python
translate(q: str, sl: str = "auto", tl: str = "zh-CN", **kwargs) -> str
```
- `q`: 需要翻译的文本
- `sl`: 源语言代码，默认`"auto"`自动检测
- `tl`: 目标语言代码，默认`"zh-CN"`（简体中文）
- `**kwargs`: 传递给`requests.get()`的额外参数

## 支持的语言

主要语言：en(英语), zh-CN(简体中文), zh-TW(繁体中文), ja(日语), ko(韩语), fr(法语), de(德语), es(西班牙语), ru(俄语), ar(阿拉伯语)等100+种语言。

完整列表请参考 [Google Translate 支持的语言](https://cloud.google.com/translate/docs/languages)。

## 注意事项

- 需要 Python 3.10+
- 由于使用非官方API，存在法律和稳定性风险
- 建议控制请求频率，避免IP被封禁
- 不建议在商业项目中直接使用

## 测试

```bash
# 运行所有测试
uv run pytest

# 运行单元测试
uv run pytest -m "not integration"

# 生成覆盖率报告
uv run pytest --cov=google_translate --cov-report=html
```
