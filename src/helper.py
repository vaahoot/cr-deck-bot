import unicodedata

from playwright.async_api import Browser, Playwright


async def init_browser(playwright: Playwright) -> Browser:
    chromium = playwright.chromium
    browser = await chromium.launch(headless=False)

    return browser


def normalise(text: str) -> str:
    return unicodedata.normalize("NFKC", text).lower().strip()
