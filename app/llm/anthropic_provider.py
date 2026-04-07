from collections.abc import AsyncIterator

import anthropic

from app.config import settings
from app.llm.base import LLMProvider


class AnthropicProvider(LLMProvider):
    def __init__(self, model: str = None):
        self.model = model or settings.anthropic_model
        self.client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    async def generate(self, system_prompt: str, user_text: str) -> str:
        resp = await self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_text}],
        )
        return resp.content[0].text

    async def generate_stream(self, system_prompt: str, user_text: str) -> AsyncIterator[str]:
        async with self.client.messages.stream(
            model=self.model,
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_text}],
        ) as stream:
            async for text in stream.text_stream:
                yield text
