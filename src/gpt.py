from openai import AsyncOpenAI
from openai import APIStatusError

from config import PROMPT, GPT_DEFAULT_VERSION
import json
import asyncio

async def extract_player_info(client: AsyncOpenAI, image_url: str, version: str = GPT_DEFAULT_VERSION, retries: int = 3) -> dict | None:
    for attempt in range(retries):
        try:
            response = await client.chat.completions.create(
                model=version,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": PROMPT},
                            {"type": "image_url", "image_url": {"url": image_url}},
                        ],
                    }
                ],
            )
            text = response.choices[0].message.content
            if text:
                cleaned = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
                return json.loads(cleaned)
        except APIStatusError as e:
            if attempt < retries - 1:
                await asyncio.sleep(1)
            else:
                raise e
    return None
