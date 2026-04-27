from openai import OpenAI
import os


class OpenRouterClient:
    BASE_URL = "https://openrouter.ai/api/v1"
    SITE_URL = "hse.ru"
    APP_NAME = "VK Polite Bot"

    def __init__(
        self,
        api_key: str,
        model: str,
        default_system_prompt: str,
        max_message_history: int = 6,
        temperature: float = 0.3,
        max_tokens: int = 500
    ):
        self.model = model
        self.default_system_prompt = default_system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_message_history = max_message_history

        self._client = OpenAI(
            base_url=self.BASE_URL,
            api_key=api_key,
        )

        self._extra_headers = {
            "HTTP-Header": self.SITE_URL,
            "X-Title": self.APP_NAME
        }

    def is_toxic(self, user_message: str) -> bool:
        """
        Проверяет, является ли сообщение токсичным.
        Возвращает True, если токсично, иначе False.
        """
        system_prompt = (
            "Ты — ИИ-помощник для модерации сообщений. "
            "Твоя задача — определить, является ли сообщение токсичным, оскорбительным или агрессивным. "
            "Проанализируй сообщение пользователя и оцени его токсичность."
            "Ответь только 'токсично' или 'нетоксично'."
            "Не добавляй ничего. Никаких пояснений, маркдауна или кода."
        )

        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        result = response.choices[0].message.content.strip().lower()
        return result == 'токсично'
