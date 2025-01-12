# LLM Key Detection Tool

一个用于检测和测试大语言模型(LLM) API密钥的图形界面工具。

## 功能特点

- 支持检查基于 [One API](https://github.com/songquanpeng/one-api) 部署的大模型API密钥余额和使用情况
- 获取可用模型列表
- 测试模型响应
- 支持中英文界面切换
- 实时显示API调用结果
- 美观的表格展示数据

## 系统要求

- Python >= 3.10
- wxPython >= 4.2.2
- requests >= 2.32.3

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/llm-key-detection.git
cd llm-key-detection
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 运行程序：
```bash
python main.py
```

2. 在界面中输入API URL和API Key
3. 使用功能按钮进行操作：
   - 「获取额度」：查看API密钥的额度使用情况
   - 「获取模型」：获取当前可用的模型列表
   - 「模型测试」：测试特定模型的响应

## 界面预览

- 主界面包含API配置区域、功能按钮、数据显示表格和日志输出区域
- 通过菜单栏可以切换中英文界面
- 表格自动调整大小，支持彩色显示不同类型的数据

## 开发说明

本项目使用wxPython开发图形界面，主要文件结构：
- `main.py`: 主程序文件，包含GUI实现
- `pyproject.toml`: 项目配置文件
- `requirements.txt`: 依赖包列表

## License

MIT License