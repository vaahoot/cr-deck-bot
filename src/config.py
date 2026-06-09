import os

ROYALE_API_PLAYER_SEARCH = "https://royaleapi.com/player/search/results?q={0}&exact_match=on"
ROYALE_API_CLAN_SEARCH = "https://royaleapi.com/clans/search?name={0}"
CLASH_API_BATTLE_LOG = "https://api.clashroyale.com/v1/players/{0}/battlelog"
CLASH_API_CLAN_MEMBERS = "https://api.clashroyale.com/v1/clans/{0}/members"
API_KEY = os.getenv("CR_KEY")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

DISCORD_API_KEY = os.getenv("SPEEDWAGON_KEY")
