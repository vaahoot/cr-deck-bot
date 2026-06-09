from config import (
    ROYALE_API_PLAYER_SEARCH,
    ROYALE_API_CLAN_SEARCH,
    CLASH_API_BATTLE_LOG,
    CLASH_API_CLAN_MEMBERS,
    HEADERS,
)
import asyncio
import unicodedata

import aiohttp
import bs4
from playwright.async_api import Browser, Playwright, async_playwright


def normalise(text):
    return unicodedata.normalize("NFKC", text).lower().strip()


async def init_browser(playwrigth: Playwright):
    chromium = playwrigth.chromium
    browser = await chromium.launch(headless=False)

    return browser


async def search(browser: Browser, link: str, selector: str):
    page = await browser.new_page()

    await page.goto(link)
    await page.wait_for_selector(selector)
    html = await page.inner_html(selector)

    await page.close()
    return html


async def search_player_by_name(browser: Browser, name: str):
    link = ROYALE_API_PLAYER_SEARCH.format(name)
    search_result_selector = ".player_search_results__container"

    return await search(browser, link, search_result_selector)


async def search_clans_by_name(browser: Browser, clan: str):
    link = ROYALE_API_CLAN_SEARCH.format(clan)
    search_result_selector = ".three.doubling.stackable.cards"

    return await search(browser, link, search_result_selector)


def parse_players(html: str):
    soup = bs4.BeautifulSoup(html, "html.parser")
    results = soup.find_all("div", class_="player_search_results__result_container")

    players = []
    for result in results:
        header = result.find("a", class_="header")
        player_tag = result.find("div", class_="player_tag")

        name = header.text.strip() if header else None
        tag = player_tag.text.strip() if player_tag else None

        clan_and_tag = result.find("a", class_="meta")
        clan_name = (
            clan_and_tag.text.strip().split("\xa0\xa0")[0] if clan_and_tag else None
        )
        clan_tag = (
            clan_and_tag.text.strip().split("\xa0\xa0")[1] if clan_and_tag else None
        )

        if name:
            name = normalise(name)
        if clan_name:
            clan_name = normalise(clan_name)

        players.append(
            {"name": name, "tag": tag, "clan": clan_name, "clan_tag": clan_tag}
        )

    return players


def parse_clans(html: str):
    soup = bs4.BeautifulSoup(html, "html.parser")
    results = soup.find_all("div", class_="clanresult")

    clans = []
    for result in results:
        clan_tag = "%23" + str(result["data-clantag"])
        clans.append(clan_tag)

    return clans


def get_last_deck(data):
    last_battle = data[0]
    team = last_battle["team"][0]
    cards = team["cards"]
    return [card["name"] for card in cards]


def find_player_tag(players, clan):
    for player in players:
        if not clan and not player["clan"]:
            return player["tag"]

        elif clan and player["clan"] == clan.lower():
            return player["tag"]

    return None


async def get_battle_log(tag: str):
    url = CLASH_API_BATTLE_LOG.format(tag.replace("#", "%23"))

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            response.raise_for_status()
            return await response.json()


async def get_clan_members(clan_tag):
    url = CLASH_API_CLAN_MEMBERS.format(clan_tag)

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            response.raise_for_status()
            return await response.json()


def find_member_in_clan(data, name):
    members = data["items"]
    for member in members:
        if member["name"] == name:
            return member["tag"]

    return None


async def search_player_in_clans(clans, name):
    for clan_tag in clans:
        data = await get_clan_members(clan_tag)
        member_tag = find_member_in_clan(data, name)

        if member_tag:
            return member_tag

    return None


async def find_deck_by_name(browser, name, clan):
    search_players = await search_player_by_name(browser, name)
    players = parse_players(search_players)

    player_tag = find_player_tag(players, clan)

    if not player_tag:
        return None

    print(f"Found a player by name. Tag: {player_tag}")
    data = await get_battle_log(player_tag)
    deck = get_last_deck(data)
    return deck


async def find_deck_by_clan(browser, name, clan):
    search_clans = await search_clans_by_name(browser, clan)
    clans = parse_clans(search_clans)

    member_tag = await search_player_in_clans(clans, name)

    if not member_tag:
        return None

    print(f"Found player by clan. Tag: {member_tag}")
    data = await get_battle_log(member_tag)
    deck = get_last_deck(data)
    return deck


async def find_deck(browser, name, clan):
    if not clan:
        return await find_deck_by_name(browser, name, clan)

    deck = await find_deck_by_clan(browser, name, clan)
    if not deck:
        deck = await find_deck_by_name(browser, name, clan)

    return deck


async def run(playwright: Playwright):
    browser = await init_browser(playwright)

    name = input("Player name: ")
    clan = input("Player clan: ")

    deck = await find_deck_by_clan(browser, name, clan)
    if not deck:
        deck = await find_deck_by_name(browser, name, clan)

    if not deck:
        print("No deck found")
    else:
        print(deck)

    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == "__main__":
    asyncio.run(main())
