"""
Copilot API - An unofficial Python API wrapper for Microsoft Copilot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A simple and powerful Python library for interacting with Microsoft Copilot.

Basic usage:

>>> from copilot_api import Copilot
>>> copilot = Copilot()
>>> messages = [{"role": "user", "content": "Hello!"}]

:copyright: (c) 2024 by OEvortex
:license: HelpingAI License, see LICENSE for more details.
"""

__title__ = 'copilot-api'
__author__ = 'OEvortex'
__email__ = 'helpingai5@gmail.com'
__version__ = '1.0.0'
__license__ = 'HelpingAI License'
__copyright__ = 'Copyright 2024 OEvortex'

from .copilot import Copilot
from .exceptions import (
    CopilotException,
    AuthenticationError,
    ConnectionError,
    InvalidRequestError,
    RateLimitError,
    ImageError,
    ConversationError,
    TimeoutError,
    MissingRequirementsError,
)
from .utils import (
    save_conversation,
    load_conversation,
    format_message,
    validate_image,
    create_system_message,
    chunk_message,
)

__all__ = [
    'Copilot',
    'CopilotException',
    'AuthenticationError',
    'ConnectionError',
    'InvalidRequestError',
    'RateLimitError',
    'ImageError',
    'ConversationError',
    'TimeoutError',
    'MissingRequirementsError',
    'save_conversation',
    'load_conversation',
    'format_message',
    'validate_image',
    'create_system_message',
    'chunk_message',
]
