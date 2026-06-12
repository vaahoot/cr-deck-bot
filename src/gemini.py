import asyncio
import json

from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError

from config import GEMINI_PROMPT, GEMINI_DEFAULT_VERSION


async def extract_player_info(client: genai.Client, image_url: str, version: str = GEMINI_DEFAULT_VERSION, retries: int = 3) -> dict | None:
    for attempt in range(retries):
        try:
            response = await client.aio.models.generate_content(
                model=version,
                contents=[
                    types.Part.from_text(text=GEMINI_PROMPT),
                    types.Part.from_uri(file_uri=image_url),
                ],
            )

            if response.text:
                cleaned = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
                info = json.loads(cleaned)
                return info

        except (ServerError, ClientError) as e:
            if attempt < retries - 1:
                await asyncio.sleep(1)
            else:
                raise e

    return None

