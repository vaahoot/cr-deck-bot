import datetime
import unicodedata

from playwright.async_api import Browser, Playwright


async def init_browser(playwright: Playwright) -> Browser:
    chromium = playwright.chromium
    browser = await chromium.launch(headless=False)

    return browser


def normalise(text: str) -> str:
    return unicodedata.normalize("NFKC", text).lower().strip()


def print_info(msg):
    time = datetime.datetime.now()
    formatted = time.strftime("%Y-%m-%d %H:%M:%S")

    print(f"{formatted} [INFO]", end="\t")
    print(msg)


def print_error(msg):
    time = datetime.datetime.now()
    formatted = time.strftime("%Y-%m-%d %H:%M:%S")

    print(f"{formatted} [ERROR]", end="\t")
    print(msg)
