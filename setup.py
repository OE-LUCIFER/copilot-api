import os
import re
from setuptools import setup, find_packages

def get_version():
    init_py = open(os.path.join('copilot_api', '__init__.py')).read()
    metadata = dict(re.findall(r"__([a-z]+)__ = '([^']+)'", init_py))
    return metadata

metadata = get_version()

with open("README.md", encoding="utf-8") as f:
    README = f.read()

setup(
    name=metadata['title'],
    version=metadata['version'],
    description="An unofficial Python API wrapper for Microsoft Copilot",
    long_description=README,
    long_description_content_type="text/markdown",
    author=metadata['author'],
    author_email=metadata['email'],
    packages=find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
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
        "curl_cffi>=0.7.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.18.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=4.0.0",
            "mypy>=0.910",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.18.0",
            "pytest-cov>=2.12.0",
        ],
    },
    project_urls={
        "Homepage": "https://github.com/OE-LUCIFER/copilot-api",
        "Bug Tracker": "https://github.com/OE-LUCIFER/copilot-api/issues",
    },
)
