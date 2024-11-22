# 🤖 Copilot API

<div align="center">

[![PyPI version](https://badge.fury.io/py/copilot-api.svg)](https://badge.fury.io/py/copilot-api)
[![Python](https://img.shields.io/pypi/pyversions/copilot-api.svg)](https://pypi.org/project/copilot-api/)
[![License: HelpingAI](https://img.shields.io/badge/License-HelpingAI-blue.svg)](https://github.com/OE-LUCIFER/copilot-api/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/OE-LUCIFER/copilot-api)](https://github.com/OE-LUCIFER/copilot-api/stargazers)
[![Downloads](https://static.pepy.tech/badge/copilot-api)](https://pepy.tech/project/copilot-api)
[![Downloads/Month](https://static.pepy.tech/badge/copilot-api/month)](https://pepy.tech/project/copilot-api)
[![Downloads/Week](https://static.pepy.tech/badge/copilot-api/week)](https://pepy.tech/project/copilot-api)
[![Last Commit](https://img.shields.io/github/last-commit/OE-LUCIFER/copilot-api)](https://github.com/OE-LUCIFER/copilot-api/commits/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub issues](https://img.shields.io/github/issues/OE-LUCIFER/copilot-api)](https://github.com/OE-LUCIFER/copilot-api/issues)

<p align="center">
  <strong>🚀 A powerful, unofficial Python API wrapper for Microsoft Copilot with CLI support</strong>
</p>

[Installation](#-installation) •
[Features](#-features) •
[Quick Start](#-quick-start) •
[CLI Usage](#-cli-usage) •
[Examples](#-examples) •
[Contributing](#-contributing) •
[Support](#-support)

</div>


## ⭐ Stargazers

<div align="center">
  
[![Stargazers repo roster for @OE-LUCIFER/copilot-api](https://reporoster.com/stars/OE-LUCIFER/copilot-api)](https://github.com/OE-LUCIFER/copilot-api/stargazers)

</div>

## 📦 Installation

```bash
# Using pip
pip install copilot-api

# From source
git clone https://github.com/OE-LUCIFER/copilot-api.git
cd copilot-api
pip install -e .
```

## 🎯 Key Features

- 🤖 **Microsoft Copilot Integration** - Direct access to Microsoft Copilot's capabilities
- 🔄 **Streaming Support** - Real-time response streaming for better interactivity
- 🛡️ **Robust Error Handling** - Comprehensive exception handling with custom error types
- 🔌 **Flexible Configuration** - Support for proxies, timeouts, and custom settings
- 🎨 **Rich CLI Interface** - Interactive terminal experience with syntax highlighting
- 📦 **Lightweight & Fast** - Minimal dependencies with efficient implementation

## ✨ Features

### Core Features
- 🔄 **Stream Chat Completions** - Real-time streaming responses
- 💬 **Conversation Management** - Maintain context across messages
- 🔒 **Proxy Support** - Configure custom proxy settings
- ⚙️ **Customizable** - Flexible timeout and configuration options

### CLI Features
- 🎨 **Rich Text Interface** - Beautiful terminal UI with syntax highlighting
- 📝 **Interactive Chat** - Full-featured chat interface in your terminal
- 💾 **Session Management** - Save and load conversation sessions
- 🎯 **Multiple Commands** - Dedicated commands for different functionalities
- 🔍 **Help System** - Built-in help and documentation

### Developer Features
- 🛠️ **Type Hints** - Full type annotation support
- 📚 **Rich Documentation** - Comprehensive API documentation
- 🧪 **Exception Handling** - Detailed error messages and handling
- 🔌 **Extensible** - Easy to extend and customize
- 🎮 **Multiple Interfaces** - Use as library or CLI tool

## 🔧 Technical Details

### Core Components

- `copilot.py` - Main Copilot client implementation
- `cli.py` - Command-line interface implementation
- `exceptions.py` - Custom exception definitions
- `utils.py` - Helper functions and utilities

### Error Handling

The library includes custom exceptions for better error management:
```python
from copilot_api.exceptions import CopilotError, AuthenticationError, APIError

try:
    response = copilot.create_completion(messages=messages)
except AuthenticationError:
    print("Authentication failed. Please check your credentials.")
except APIError as e:
    print(f"API error occurred: {e}")
```

## 🚀 Quick Start

### Python Library Usage

```python
from copilot_api import Copilot

# Initialize Copilot
copilot = Copilot()

# Basic chat example
messages = [
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": "Hello!"}
]

# Stream responses
for response in copilot.create_completion(
    model="Copilot",
    messages=messages,
    stream=True
):
    if isinstance(response, str):
        print(response, end='', flush=True)
```

## 🖥️ CLI Usage

### Interactive Chat

```bash
# Start interactive chat
copilot-cli

# Start chat with specific model
copilot-cli --model Copilot

# Save conversation
copilot-cli --save chat_history.json

# Load previous conversation
copilot-cli --load chat_history.json
```

### Alternative Usage
```bash
# Using Python module directly
python -m copilot_api.cli chat

# Or using the main command
copilot chat
```

### CLI Commands
- `/help` - Show help message
- `/clear` - Clear current conversation
- `/save <filename>` - Save conversation
- `/load <filename>` - Load conversation
- `/exit` - Exit the CLI

## 📚 Examples

### 💬 Managing Conversations

```python
from copilot_api import save_conversation, load_conversation

# Save conversation
save_conversation("chat_history.json", messages)

# Load conversation
messages = load_conversation("chat_history.json")
```

## 🛠️ Advanced Usage

### Proxy Configuration
```python
copilot = Copilot(
    proxy="http://your-proxy-server:port"
)
```

### Custom Timeout Settings
```python
copilot = Copilot(
    timeout=30  # seconds
)
```

### Advanced Configuration

```python
from copilot_api import Copilot

# Initialize with custom configuration
copilot = Copilot(
    timeout=30,
    proxy="http://proxy:port",
    max_retries=3,
    verify_ssl=True
)

# Custom headers and parameters
response = copilot.create_completion(
    messages=[{"role": "user", "content": "Hello!"}],
    stream=True,
    temperature=0.7,
    max_tokens=150
)
```

### CLI Features

The CLI tool (`copilot-cli`) supports various commands and options:

```bash
# Start with custom configuration
copilot-cli --timeout 30 --no-stream

# Export conversation
copilot-cli --export chat.json

# Import and continue conversation
copilot-cli --import chat.json
```

Available CLI commands:
- `/system <message>` - Set system message
- `/model <name>` - Change model
- `/retry` - Retry last message
- `/tokens` - Show token count
- `/version` - Show version info

## 🔍 Debugging

Enable debug mode for detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

copilot = Copilot(debug=True)
```

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install -e ".[test]"

# Run tests with coverage
pytest --cov=copilot_api tests/
```

## 📋 Requirements

- Python 3.7+
- Core Dependencies:
  - `requests>=2.25.0`
  - `websockets>=10.0`
  - `aiohttp>=3.8.0`
  - `python-dotenv>=0.19.0`
  - `tls-client>=0.2.0`
  - `beautifulsoup4>=4.9.3`
- CLI Dependencies:
  - `click>=8.0.0`
  - `rich>=10.0.0`
  - `prompt-toolkit>=3.0.0`

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone https://github.com/OE-LUCIFER/copilot-api.git

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## 📝 License

This project is licensed under the HelpingAI License - see the [LICENSE](LICENSE) file for details.

The HelpingAI License is a proprietary license that grants specific rights while protecting HelpingAI's intellectual property. Please read the license carefully before using this software.

## 🌟 Support

- Star this repository
- Follow [@OEvortex](https://youtube.com/@OEvortex) on YouTube
- Report issues on our [Issue Tracker](https://github.com/OE-LUCIFER/copilot-api/issues)
- Consider [sponsoring](https://github.com/sponsors/OE-LUCIFER) the project

## 📊 Project Stats

![Alt](https://repobeats.axiom.co/api/embed/ff8173c0c516e81b66502ce32e1b386dd3da2fdc.svg "Repobeats analytics image")

## 📈 Star History

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=OE-LUCIFER/copilot-api&type=Date)](https://star-history.com/#OE-LUCIFER/copilot-api&Date)

</div>

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/OE-LUCIFER">OEvortex</a></sub>
</div>
