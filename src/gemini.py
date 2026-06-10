import asyncio
import json

from google import genai
from google.genai import types
from google.genai.errors import ServerError

from config import PROMPT


async def extract_player_info(client: genai.Client, image_url: str, retries: int = 3) -> dict | None:
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=[
                    types.Part.from_text(text=PROMPT),
                    types.Part.from_uri(file_uri=image_url),
                ],
            )

            if response.text:
                cleaned = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
                info = json.loads(cleaned)
                return info

        except ServerError as e:
            if attempt < retries - 1:
                await asyncio.sleep(2)
            else:
                raise e

    return None

