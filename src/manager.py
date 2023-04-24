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
        self._driver.implicitly_wait(20) 

    def generate_message(self, context: list[str], name: str) -> str:
        messages = "\n".join(context)
        
        past = self._archive[name]["context"]
        new_context = ""
        if past:
            new_context = f"\n\nThe following is the context of this conversation, you are talking to {name}. The last message was from you."
            for i in past:
                new_context += '\n\n' + i
        
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model=self._model,
                    messages=[
                        {"role": "system", "content": self._gpt_preset + new_context},
                        {"role": "user", "content": messages},
                    ],
                )
                break
            except Exception as e:
                print(e)
        
        reply = response["choices"][0]["message"]["content"]
        self._archive[name]["context"].extend([messages, reply])
        return str(reply).lower()

    def is_convo_over(self, messages: list[str]) -> bool:
        message = "\n".join(messages)
        response = openai.ChatCompletion.create(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": "Reply True or False or Unsure for the following questions.",
                },
                {"role": "user", "content": f"Does '{message}' suggest a conversation has ended?"},
            ],
        )
        print(response["choices"][0]["message"]["content"].lower())
        return "true" in response["choices"][0]["message"]["content"].lower()
