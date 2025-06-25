import abc
import os

import openai


# --- GiftProvider: интерфейс для получения идеи подарка ---
class GiftProvider(abc.ABC):
    @abc.abstractmethod
    def get_random_gift(self) -> str:
        """Вернуть строку с идеей подарка."""
        pass


class AIProvider(GiftProvider):
    """
    Генерирует идеи подарков через OpenAI API.
    """

    def __init__(self):
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY not set")
        openai.api_key = key

    def get_random_gift(self) -> str:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "Ты — генератор идей простых подарков до $5."
                    " Каждый раз предлагай нечто новое и неожиданное."
                )},
                {"role": "user", "content": "Предложи идею подарка."}
            ],
            max_tokens=50,
            temperature=0.8,
        )
        return resp.choices[0].message.content.strip()
