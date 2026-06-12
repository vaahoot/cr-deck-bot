from PIL import Image
import aiohttp
import io


def get_last_deck(data: list[dict] | None) -> list[dict[str, str]] | None:
    if not data:
        return None

    last_battle = dict()
    for battle in data:
        if battle.get("type") == "pathOfLegend":
            last_battle = battle
            break

    if not last_battle:
        for battle in data:
            if battle.get("type") == "PvP":
                last_battle = battle
                break

    if not last_battle:
        return None


    team = last_battle["team"][0]
    cards = team["cards"]

    deck = []
    for card in cards:
        name = card["name"]

        # Temporary because supercell messed up evo princess and hero tombstone images
        if name == "Princess" or name == "Tombstone":
            deck.append({"name": name, "imgLink": card["iconUrls"]["medium"]})
            continue

        if card.get("evolutionLevel") == 1:
            deck.append({"name": name, "imgLink": card["iconUrls"]["evolutionMedium"]})
        elif card.get("evolutionLevel") == 2:
            deck.append({"name": name, "imgLink": card["iconUrls"]["heroMedium"]})
        else:
            deck.append({"name": name, "imgLink": card["iconUrls"]["medium"]})

    return deck


async def fetch_image(url: str) -> Image.Image:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            return Image.open(io.BytesIO(data))


async def build_deck_image(cards: list[dict]) -> Image.Image:
    images = [await fetch_image(card["imgLink"]) for card in cards]

    width = sum(img.width for img in images) // 2
    height = max(img.height for img in images) * 2

    combined = Image.new("RGBA", (width, height))
    x = 0
    y = 0
    for img in images:
        if x >= width:
            x = 0
            y = height // 2

        combined.paste(img, (x, y))
        x += img.width

    return combined
