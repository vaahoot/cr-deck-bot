import os
from pathlib import Path

ROYALE_API_PLAYER_SEARCH = "https://royaleapi.com/player/search/results?q={0}&exact_match=on"
ROYALE_API_CLAN_SEARCH = "https://royaleapi.com/clans/search?name={0}"
CLASH_API_BATTLE_LOG = "https://proxy.royaleapi.dev/v1/players/{0}/battlelog"
CLASH_API_CLAN_MEMBERS = "https://proxy.royaleapi.dev/v1/clans/{0}/members"

CLASH_API_KEY = os.getenv("CR_KEY")
CLASH_API_HEADERS = {"Authorization": f"Bearer {CLASH_API_KEY}"}

DISCORD_API_KEY = os.getenv("DISCORD_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_KEY")

GEMINI_DEFAULT_VERSION = "gemini-2.5-flash"
GEMINI_PROMPT = """You are analyzing a Clash Royale matchmaking screen. Two players are shown battling.
Extract the name and clan of the OPPONENT only. The opponent is the player on the TOP half of the screen.
The opponent's player name appears prominently in gold or white text. Directly below it is their clan name in a smaller, yellowish font. Below the clan name is their King level.
Return ONLY a valid JSON object with no markdown, no explanation, no code blocks:
{"name": "player_name", "clan": "clan_name"}
Rules:
- If no clan is visible, set clan to null
- If this is not a Clash Royale matchmaking screen, return {"name": null, "clan": null}
- Preserve the exact spelling and capitalisation of the name and clan
- Do not confuse the bottom player (you) with the top player (opponent)"""

PREFERENCES = Path(__file__).parent.parent / "preferences.json"

