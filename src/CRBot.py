from discord.ext import commands
from playwright.async_api import Browser, Playwright, async_playwright

import helper


class CRBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix, intents=intents)
        self.browser: Browser | None = None
        self.playwright: Playwright | None = None

    async def setup_hook(self):
        self.playwright = await async_playwright().start()
        print(f"[INFO] Created playwright: {self.playwright}")
        self.browser = await helper.init_browser(self.playwright)
        print(f"[INFO] Created a browser: {self.browser}")

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        await super().close()
