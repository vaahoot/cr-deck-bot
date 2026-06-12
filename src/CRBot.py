import asyncio
import aiofiles
import io
import json
import os

import discord
from discord.ext import commands
from google.genai.errors import ClientError, ServerError
from playwright.async_api import Browser, Playwright, async_playwright

import helper
import search
from config import PREFERENCES
from deck import build_deck_image
from gemini import extract_player_info
from helper import print_error, print_info


def load_preferences() -> dict:
    if not os.path.exists(PREFERENCES):
        return {}
    with open(PREFERENCES, "r") as f:
        return json.load(f)


async def save_preferences(data: dict) -> None:
    async with aiofiles.open(PREFERENCES, "w") as f:
        await f.write(json.dumps(data))


class CRBot(commands.Bot):
    def __init__(self, command_prefix, intents, gemini_client):
        super().__init__(command_prefix, intents=intents)
        self.browser: Browser | None = None
        self.playwright: Playwright | None = None
        self.gemini_client = gemini_client

    async def setup_hook(self):
        self.playwright = await async_playwright().start()
        print_info(f"Created playwright: {self.playwright}")
        self.browser = await helper.init_browser(self.playwright)
        print_info(f"Created a browser: {self.browser}")

        self.preferences = load_preferences()
        print_info("Preferences loaded")

    async def search_by_info(self, name: str, clan: str | None, message):
        assert self.browser is not None
        print_info(f"Searching for: {name}, Clan: {clan if clan else 'No clan'}")
        channel = message.channel

        async with channel.typing():
            deck = await search.find_deck(self.browser, name, clan)

            if not deck:
                await message.reply("No deck found")
                return

            print_info(f"Found deck for {name}: {[card['name'] for card in deck]}")
            deck_image = await build_deck_image(deck)
            buffer = io.BytesIO()
            deck_image.save(buffer, format="PNG")
            buffer.seek(0)

        await message.reply(file=discord.File(buffer, filename="deck.png"))

    async def search_by_image(self, message):
        assert self.browser is not None

        attachments = message.attachments
        channel = message.channel

        async with channel.typing():
            url = attachments[0].url

            try:
                player_info = await extract_player_info(self.gemini_client, url)
            except ClientError as e:
                print_error(f"ClientError: {e.code} {e.status}")
                await message.reply("Gemini limit reached")
                return
            except ServerError as e:
                print_error(f"ServerError: {e.code} {e.status}")
                await message.reply("Gemini servers are busy, try again later")
                return

            if not player_info:
                await message.reply("Internal Error")
                return

            name = player_info.get("name")
            clan = player_info.get("clan")

            if not name:
                print_error("Invalid image received")
                await message.reply("Invalid image")
                return

            await self.search_by_info(name, clan, message)

    async def on_message(self, message):
        if message.author == self.user:
            return

        guild = message.guild.id
        channel = message.channel.id

        if (channel in self.preferences.setdefault(str(guild), []) and message.attachments):
            asyncio.create_task(self.search_by_image(message))

        await self.process_commands(message)

    async def close(self):
        if self.browser:
            await self.browser.close()
            print_info("Closed browser")
        if self.playwright:
            await self.playwright.stop()
            print_info("Closed playwright")

        await super().close()
