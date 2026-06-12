import datetime
import json
import os
import unicodedata

import aiofiles
from colorama import Fore, Style
from playwright.async_api import Browser, Playwright

from config import PREFERENCES


async def init_browser(playwright: Playwright) -> Browser:
    chromium = playwright.chromium
    browser = await chromium.launch(headless=False)

    return browser


def normalise(text: str) -> str:
    return unicodedata.normalize("NFKC", text).lower().strip()


def log(msg, color, type):
    time = datetime.datetime.now()
    formatted = time.strftime("%Y-%m-%d %H:%M:%S")

    print(Style.DIM + f"{formatted}" + Style.RESET_ALL, end=" ")
    print(color + type + Style.RESET_ALL, end="\t")
    print(msg, end="")
    print(Style.RESET_ALL)


def print_info(msg):
    log(msg, Fore.GREEN, "INFO")


def print_error(msg):
    log(msg, Fore.RED, "ERROR")


def load_preferences() -> dict:
    if not os.path.exists(PREFERENCES):
        return {}
    with open(PREFERENCES, "r") as f:
        return json.load(f)


async def save_preferences(data: dict) -> None:
    async with aiofiles.open(PREFERENCES, "w") as f:
        await f.write(json.dumps(data))
