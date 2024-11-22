from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    README = f.read()

setup(
    name="copilot-api",
    version="0.1.0",
    description="An unofficial Python API wrapper for Microsoft Copilot",
    long_description=README,
    long_description_content_type="text/markdown",
    author="OEvortex",
    author_email="helpingai5@gmail.com",
    packages=find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
    ],
    install_requires=[
        "requests>=2.25.0",
        "websockets>=10.0",
        "aiohttp>=3.8.0",
        "python-dotenv>=0.19.0",
        "tls-client>=0.2.0",
        "beautifulsoup4>=4.9.3",
        "pillow>=8.0.0",
        "click>=8.0.0",
        "rich>=10.0.0",
        "prompt-toolkit>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.18.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=4.0.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    project_urls={
        "Source": "https://github.com/OE-LUCIFER/copilot-api",
        "Tracker": "https://github.com/OE-LUCIFER/copilot-api/issues",
        "YouTube": "https://youtube.com/@OEvortex",

        "Changelog": "https://github.com/OE-LUCIFER/copilot-api/releases",
        "Funding": "https://github.com/sponsors/OE-LUCIFER",
    },
    keywords=["copilot", "api", "chatbot", "microsoft", "ai", "assistant"],
    entry_points={
        "console_scripts": [
            "copilot=copilot_api.cli:cli",
            "copilot-cli=copilot_api.cli:chat",
        ],
    },
)
