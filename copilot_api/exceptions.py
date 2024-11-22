"""Exceptions for Copilot API."""

class CopilotException(Exception):
    """Base exception for Copilot API."""
    pass

class AuthenticationError(CopilotException):
    """Raised when authentication fails."""
    pass

class ConnectionError(CopilotException):
    """Raised when connection to Copilot fails."""
    pass

class InvalidRequestError(CopilotException):
    """Raised when request is invalid."""
    pass

class RateLimitError(CopilotException):
    """Raised when rate limit is exceeded."""
    pass

class ImageError(CopilotException):
    """Raised when there's an error with image processing."""
    pass

class ConversationError(CopilotException):
    """Raised when there's an error with conversation management."""
    pass

class TimeoutError(CopilotException):
    """Raised when request times out."""
    pass

class MissingRequirementsError(Exception):
    """Raised when required dependencies are not installed."""
    pass
