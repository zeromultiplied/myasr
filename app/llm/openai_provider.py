from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from app.config import settings
from app.llm.base import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self, model: str = None):
        self.model = model or settings.openai_model
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
        )

    async def generate(self, system_prompt: str, user_text: str) -> str:
        resp = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text},
            ],
        )
        return resp.choices[0].message.content

    async def generate_stream(self, system_prompt: str, user_text: str) -> AsyncIterator[str]:
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text},
            ],
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content
