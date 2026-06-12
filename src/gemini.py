import asyncio
import json

from google import genai
from google.genai import types
from google.genai.errors import ServerError, ClientError

from config import PROMPT


async def extract_player_info(client: genai.Client, image_url: str, retries: int = 3) -> dict | None:
    for attempt in range(retries):
        try:
            response = await client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_text(text=PROMPT),
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

