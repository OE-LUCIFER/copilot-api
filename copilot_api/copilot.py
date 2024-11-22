from typing import Optional, Dict, List, Union, Generator, Any, TypeVar, Type
from abc import ABC, abstractmethod
from http.cookiejar import CookieJar
import json
from urllib.parse import quote
import threading
from dataclasses import dataclass
from curl_cffi.requests import Session, CurlWsFlag
import requests
import time
from queue import Queue
import os

from .exceptions import MissingRequirementsError
from .utils import (
    raise_for_status,
    format_cookies,
    format_prompt,
    to_bytes,
    is_accepted_format,
)

# Type definitions
Messages = List[Dict[str, str]]
ImageType = Union[str, bytes]
T = TypeVar('T')

@dataclass
class ImageResponse:
    url: str
    prompt: str
    metadata: Dict[str, Any]

class CreateResult(Generator):
    def __init__(self, gen):
        self._gen = gen
        
    def send(self, value):
        return next(self._gen)
        
    def throw(self, typ, val=None, tb=None):
        if val is None:
            val = typ()
        if tb is None:
            return self._gen.throw(typ, val)
        return self._gen.throw(typ, val, tb)
        
    def close(self):
        return self._gen.close()

class BaseConversation:
    pass

class AbstractProvider(ABC):
    label: str
    url: str
    working: bool
    supports_stream: bool
    default_model: str
    needs_auth: bool = True

    @abstractmethod
    def create_completion(self, *args, **kwargs) -> CreateResult:
        pass

class Conversation(BaseConversation):
    def __init__(self, conversation_id: str, cookie_jar: CookieJar, access_token: str = None):
        self.conversation_id = conversation_id
        self.cookie_jar = cookie_jar
        self.access_token = access_token
        self._lock = threading.Lock()
        self._cookies_dict = {}
        self._update_cookies_dict()

    def _update_cookies_dict(self):
        self._cookies_dict = {cookie.name: cookie.value for cookie in self.cookie_jar}

    def update_token(self, new_token: str):
        with self._lock:
            self.access_token = new_token
            self._update_cookies_dict()

    @property
    def cookies(self):
        return self._cookies_dict

class TokenManager:
    def __init__(self):
        self._token = None
        self._cookies = None
        self._lock = threading.Lock()
        self._token_queue = Queue()

    def get_token_and_cookies(self, proxy: str = None) -> tuple[str, Dict[str, str]]:
        with self._lock:
            if self._token and self._cookies:
                return self._token, self._cookies
            
            session = requests.Session()
            if proxy:
                session.proxies = {"http": proxy, "https": proxy}

            response = session.get("https://copilot.microsoft.com")
            response.raise_for_status()

            local_storage_data = {
                "credentialType": "AccessToken",
                "secret": "dummy_token_for_demo"
            }

            self._token = local_storage_data["secret"]
            self._cookies = session.cookies.get_dict()

            return self._token, self._cookies

class Copilot(AbstractProvider):
    label = "Microsoft Copilot"
    url = "https://copilot.microsoft.com"
    working = True
    supports_stream = True
    default_model = "Copilot"
    websocket_url = "wss://copilot.microsoft.com/c/api/chat?api-version=2"
    conversation_url = f"{url}/c/api/conversations"
    _token_manager = TokenManager()

    def __init__(self, config_file: str = 'config.json'):
        self.config = {}
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                self.config = json.load(f)

    def create_completion(
            self,
            model: str,
            messages: Messages,
            stream: bool = False,
            proxy: str = None,
            timeout: int = 900,
            image: ImageType = None,
            conversation: Optional[Conversation] = None,
            return_conversation: bool = False,
            web_search: bool = True,
            **kwargs
        ):
        """Create a completion for the chat conversation."""
        try:
            has_curl_cffi = True
            if not has_curl_cffi:
                raise MissingRequirementsError('Install curl_cffi package')

            # Apply configuration if available
            if self.config.get('persona'):
                system_message = {
                    "role": "system",
                    "content": self.config['persona']
                }
                messages = [system_message] + messages

            if self.config.get('context'):
                context_message = {
                    "role": "system",
                    "content": self.config['context']
                }
                messages = [context_message] + messages

            if self.config.get('temperature'):
                kwargs['temperature'] = self.config['temperature']

            websocket_url = self.websocket_url
            access_token = None
            headers = None
            cookies = conversation.cookie_jar if conversation is not None else None

            if self.needs_auth or image is not None:
                if conversation is None or conversation.access_token is None:
                    access_token, cookies = self._token_manager.get_token_and_cookies(proxy)
                else:
                    access_token = conversation.access_token
                    cookies = conversation.cookies
                
                websocket_url = f"{websocket_url}&accessToken={quote(access_token)}"
                headers = {"authorization": f"Bearer {access_token}", "cookie": format_cookies(cookies)}

            with Session(
                timeout=timeout,
                proxy=proxy,
                impersonate="chrome",
                headers=headers,
                cookies=cookies,
            ) as session:
                response = session.get(f"{self.url}/c/api/user")
                raise_for_status(response)

                if conversation is None:
                    response = session.post(self.conversation_url)
                    raise_for_status(response)
                    conversation_id = response.json().get("id")
                    if return_conversation:
                        yield Conversation(conversation_id, session.cookies.jar, access_token)
                    prompt = format_prompt(messages)
                else:
                    conversation_id = conversation.conversation_id
                    prompt = messages[-1]["content"]

                images = []
                if image is not None:
                    data = to_bytes(image)
                    response = session.post(
                        f"{self.url}/c/api/attachments",
                        headers={"content-type": is_accepted_format(data)},
                        data=data
                    )
                    raise_for_status(response)
                    images.append({"type": "image", "url": response.json().get("url")})

                wss = session.ws_connect(websocket_url)
                wss.send(json.dumps({
                    "event": "send",
                    "conversationId": conversation_id,
                    "content": [*images, {
                        "type": "text",
                        "text": prompt,
                    }],
                    "mode": "chat"
                }).encode(), CurlWsFlag.TEXT)

                is_started = False
                msg = None
                image_prompt: str = None
                last_msg = None

                while True:
                    try:
                        msg = wss.recv()[0]
                        msg = json.loads(msg)
                    except Exception as e:
                        break

                    last_msg = msg
                    if msg.get("event") == "appendText":
                        is_started = True
                        yield msg.get("text")
                    elif msg.get("event") == "generatingImage":
                        image_prompt = msg.get("prompt")
                    elif msg.get("event") == "imageGenerated":
                        yield ImageResponse(msg.get("url"), image_prompt, {"preview": msg.get("thumbnailUrl")})
                    elif msg.get("event") == "done":
                        break
                    elif msg.get("event") == "error":
                        raise RuntimeError(f"Error: {msg}")

                if not is_started:
                    raise RuntimeError(f"Invalid response: {last_msg}")

        except Exception as e:
            raise
