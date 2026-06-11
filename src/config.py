import os

ROYALE_API_PLAYER_SEARCH = "https://royaleapi.com/player/search/results?q={0}&exact_match=on"
ROYALE_API_CLAN_SEARCH = "https://royaleapi.com/clans/search?name={0}"
CLASH_API_BATTLE_LOG = "https://proxy.royaleapi.dev/v1/players/{0}/battlelog"
CLASH_API_CLAN_MEMBERS = "https://proxy.royaleapi.dev/v1/clans/{0}/members"
API_KEY = os.getenv("CR_KEY")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

DISCORD_API_KEY = os.getenv("DISCORD_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_KEY")


PROMPT = """You are analyzing a Clash Royale screenshot. Extract the opponent's player name and clan name. Return ONLY a JSON object with exactly these two fields: {"name": "player_name", "clan": "clan_name"}. If no clan is visible, set clan to null. Do not include any other text, explanation, or markdown formatting in your response. If a picture is not from clash royale or the name and clan are not visible, return null for both."""
