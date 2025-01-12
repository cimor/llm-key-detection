# LLM Key Detection Tool

A GUI tool for detecting and testing Large Language Model (LLM) API keys.

## Features

- Support for checking API key balance and usage for LLM APIs deployed with [One API](https://github.com/songquanpeng/one-api)
- Retrieve available model lists
- Test model responses
- Support for Chinese and English interface switching
- Real-time display of API call results
- Elegant table data presentation

## System Requirements

- Python >= 3.10
- wxPython >= 4.2.2
- requests >= 2.32.3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/llm-key-detection.git
cd llm-key-detection
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the program:
```bash
python main.py
```

2. Enter API URL and API Key in the interface
3. Use function buttons to perform operations:
   - "Check Balance": View API key quota usage
   - "Get Models": Retrieve list of available models
   - "Test Model": Test specific model responses

## Interface Preview

- Main interface includes API configuration area, function buttons, data display table, and log output area
- Language can be switched between Chinese and English via menu bar
- Tables automatically adjust size and support colored display for different types of data

## Development Notes

This project uses wxPython for GUI development, with the following main file structure:
- `main.py`: Main program file containing GUI implementation
- `pyproject.toml`: Project configuration file
- `requirements.txt`: List of dependencies

## License

MIT License