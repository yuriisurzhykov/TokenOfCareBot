# src/adapter/service/ai_gift_generator.py
import random
from typing import List

from src.domain.model.gift_idea import GiftIdea
from src.domain.service.gift_generator import GiftGenerator
from src.infrastructure.openai.openai_service import OpenAIService


class OpenAIGiftGenerator(GiftGenerator):
    """
    Генератор идей подарков на базе OpenAI.
    Запрашивает сразу несколько вариантов, а затем выбирает случайный.
    """

    def __init__(self, ai: OpenAIService, options_count: int = 5):
        self.ai = ai
        self.options_count = options_count

    def generate(self) -> GiftIdea:
        # Запросить несколько идей и выбрать одну случайно
        prompt = (
            f"Ты — генератор идей простых подарков для жены до $5. "
            f"Предложи {self.options_count} разных идей. "
            "Каждая идея — короткое словосочетание (1–5 слов), перечисли через новую строку."
        )
        response = self.ai.ask(prompt)
        # Разбить по строкам и очистить от буллитов/номеров
        lines = [line.strip('-•0123456789. ') for line in response.splitlines()]
        options: List[str] = [line for line in lines if line]

        if options:
            # Собираем единый текст с пунктами
            formatted = '\n'.join(f"- {opt}" for opt in options)
            text = f"Вот варианты подарков:\n{formatted}"
        else:
            # fallback: отправляем чистый ответ
            text = response.strip()
        return GiftIdea(text=text)
