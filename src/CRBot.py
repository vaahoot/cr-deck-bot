import io

import discord
from discord.ext import commands
from google.genai.errors import ClientError, ServerError
from playwright.async_api import Browser, Playwright, async_playwright

from config import GEMINI_DEFAULT_VERSION
import helper
import search
from deck import build_deck_image
from gemini import extract_player_info
from helper import load_preferences, print_error, print_info, save_preferences


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
        guild = message.guild

        async with channel.typing():
            url = attachments[0].url
            preferences = self.get_preferences(guild.id)
            gemini_version = preferences.setdefault("geminiVersion", GEMINI_DEFAULT_VERSION)

            try:
                player_info = await extract_player_info(self.gemini_client, url, gemini_version)
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

    async def save_preferences(self):
        await save_preferences(self.preferences)

    def get_preferences(self, guild_id: int):
        """Return a list of all preferences saved in the bot for a given guild"""
        guild_key = str(guild_id)
        return self.preferences.setdefault(guild_key, {})

    async def on_message(self, message):
        if message.author == self.user:
            return

        guild = message.guild.id
        channel = message.channel.id
        preferences = self.get_preferences(guild)

        if (channel in preferences.setdefault("imageChannels", []) and message.attachments):
            await self.search_by_image(message)

        await self.process_commands(message)

    async def close(self):
        if self.browser:
            await self.browser.close()
            print_info("Closed browser")
        if self.playwright:
            await self.playwright.stop()
            print_info("Closed playwright")

        await super().close()
