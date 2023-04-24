from abc import ABC, abstractmethod
from selenium import webdriver
from typing import Any
import openai

SYSTEM = "You are to treat this conversation as a message exchange between young adults on snapchat. As in, you are pretending to be a young adult using snapchat. The implications of that are you will provide short responses with no capitalization, lots of acronyms, limited punctuation, slang and no emojiis. You are to act as a snapchat user."
MODEL = "gpt-3.5-turbo"


    
class Manager(ABC):
    """
    Interface for API classes
    """
    _driver: Any
    _state: Any
    _model: str
    _gpt_preset: str
    _archive: dict
    _order: list[str]
    
    def __init__(self, driver: Any, model: str = MODEL, gpt_preset: str = SYSTEM) -> None:
        self._driver = driver
        self._model = model
        self._gpt_preset = gpt_preset
        self._state = None
        self._archive = {}
        self._order = []

    @abstractmethod
    def send_message(self, message) -> None:
        pass

    @abstractmethod
    def get_messages(self) -> list[str]:
        pass
    
    @abstractmethod
    def access_conversation(self) -> None:
        pass
    
    @abstractmethod
    def close_conversation(self) -> None:
        pass
    
    @abstractmethod
    def update_conversation(self) -> None:
        pass
    
    @abstractmethod
    def monitor(self) -> None:
        pass
    
    def wait(self) -> None:
        self._driver.implicitly_wait(10) 

    def generate_message(self, context: list[str]) -> str:
        messages = "\n".join(context)
        response = openai.ChatCompletion.create(
            model=self._model,
            messages=[
                {"role": "system", "content": self._gpt_preset},
                {"role": "user", "content": messages},
            ],
        )

        return response["choices"][0]["message"]["content"]

    def is_convo_over(self, message) -> bool:
        response = openai.ChatCompletion.create(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": "Reply True or False for the following questions.",
                },
                {"role": "user", "content": f"Does {message} suggest a conversation has ended?"},
            ],
        )

        return "true" in response["choices"][0]["message"]["content"].lower()
