from typing import Dict, List, Union
from http.cookiejar import CookieJar
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

# Type definitions
Messages = List[Dict[str, str]]
ImageType = Union[str, bytes]

def raise_for_status(response):
    """Raises an exception if the response status code indicates an error."""
    if 400 <= response.status_code < 600:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

def format_cookies(cookies: Union[Dict[str, str], CookieJar]) -> str:
    """Formats cookies dictionary or CookieJar into a string for HTTP headers."""
    if isinstance(cookies, dict):
        return "; ".join([f"{k}={v}" for k, v in cookies.items()])
    elif isinstance(cookies, CookieJar):
        return "; ".join([f"{cookie.name}={cookie.value}" for cookie in cookies])
    return ""

def format_prompt(messages: Messages) -> str:
    """Formats a list of messages into a single prompt string."""
    return "\n".join([msg["content"] for msg in messages])

def to_bytes(image: ImageType) -> bytes:
    """Converts an image (file path or bytes) to bytes."""
    if isinstance(image, str):
        with open(image, 'rb') as f:
            return f.read()
    return image

def is_accepted_format(data: bytes) -> str:
    """Determines the MIME type of image data."""
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'
    elif data.startswith(b'\xff\xd8'):
        return 'image/jpeg'
    return 'application/octet-stream'

def get_config_dir() -> Path:
    """Get the configuration directory."""
    config_dir = Path.home() / '.copilot'
    config_dir.mkdir(exist_ok=True)
    return config_dir

def save_conversation(filename: str, messages: List[Dict[str, str]]) -> None:
    """Save conversation to a file."""
    if not filename.endswith('.json'):
        filename += '.json'
    
    filepath = get_config_dir() / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({
            'messages': messages,
            'version': '1.0'
        }, f, ensure_ascii=False, indent=2)

def load_conversation(filename: str) -> List[Dict[str, str]]:
    """Load conversation from a file."""
    if not filename.endswith('.json'):
        filename += '.json'
    
    filepath = get_config_dir() / filename
    
    if not filepath.exists():
        raise FileNotFoundError(f"Conversation file not found: {filename}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get('messages', [])

def format_message(message: Dict[str, str]) -> str:
    """Format a message for display."""
    role = message['role'].capitalize()
    content = message['content']
    return f"{role}: {content}"

def validate_image(image_path: str) -> bool:
    """Validate image file."""
    if not os.path.exists(image_path):
        return False
    
    valid_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
    return Path(image_path).suffix.lower() in valid_extensions

def create_system_message(instruction: str) -> Dict[str, str]:
    """Create a system message."""
    return {
        "role": "system",
        "content": instruction
    }

def chunk_message(message: str, chunk_size: int = 2000) -> List[str]:
    """Split a message into chunks of specified size."""
    return [message[i:i + chunk_size] for i in range(0, len(message), chunk_size)]
