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
GEMINI_PROMPT = """You are analyzing a Clash Royale matchmaking screen. There are two players shown. Extract the name and clan of the OPPONENT - this is the player on the TOP side of the screen. Return ONLY a JSON object: {"name": "player_name", "clan": "clan_name"}. If no clan is visible, set clan to null. If the name AND clan are not visible or the screenshot doesn't show clash royale gameplay, set both to null. Do not include any other text, explanation, or markdown formatting. The player name is displayed prominently above the clan name which is smaller. The player name is either gold or white and the clan name has a yellowish colour."""

PREFERENCES = Path(__file__).parent.parent / "preferences.json"
