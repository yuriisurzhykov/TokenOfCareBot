# src/infrastructure/openai/openai_service.py

import os
from typing import List, Dict, Optional

import openai


class OpenAIService:
    """
    Обёртка над OpenAI ChatCompletion API.
    Параметры frequency_penalty и присутствия помогают снизить повторяемость.
    """

    def __init__(
            self,
            api_key: Optional[str] = None,
            model: str = "gpt-4.1-nano",
            temperature: float = 1.0,
            max_tokens: int = 150,
            frequency_penalty: float = 1.0,
            presence_penalty: float = 0.5,
            top_p: float = 1.0,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        openai.api_key = self.api_key

        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.top_p = top_p

    def ask_chat(self, messages: List[Dict[str, str]]) -> str:
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            top_p=self.top_p,
        )
        return resp.choices[0].message.content.strip()

    def ask(self, prompt: str) -> str:
        return self.ask_chat([{"role": "user", "content": prompt}])
