import io

import discord
from google import genai

import search
from config import DISCORD_API_KEY, GEMINI_API_KEY
from CRBot import CRBot
from deck import build_deck_image
from gemini import extract_player_info

if not DISCORD_API_KEY:
    raise ValueError("API key not found")

browser = None

intents = discord.Intents.default()
intents.message_content = True

bot = CRBot(command_prefix="!", intents=intents)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)


@bot.command()
async def d(ctx):
    if not bot.browser:
        print("[ERROR] No browser is initialized")
        await ctx.reply("Internal Error")
        return

    message = ctx.message.content
    message_without_command = message[2:]

    args = message_without_command.split(",")

    if len(args) == 2:
        name = args[0].strip()
        clan = args[1].strip()
    elif len(args) == 1:
        name = args[0].strip()
        clan = None
    else:
        await ctx.reply("Invalid number of arguments")
        return


    print(f"[INFO] Searching for: {name}, Clan: {clan if clan else 'No clan'}")

    async with ctx.typing():
        deck = await search.find_deck(bot.browser, name, clan)

        if not deck:
            await ctx.reply("No deck found")
            return

        print(f"Found deck for {name}: {[card['name'] for card in deck]}")
        deck_image = await build_deck_image(deck)
        buffer = io.BytesIO()
        deck_image.save(buffer, format="PNG")
        buffer.seek(0)

    await ctx.reply(file=discord.File(buffer, filename="deck.png"))


@bot.command()
async def i(ctx):
    if not bot.browser:
        print("[ERROR] No browser is initialized")
        await ctx.reply("Internal Error")
        return

    attachments = ctx.message.attachments

    if not attachments:
        ctx.reply("This command requires a screenshot")
        return
    if len(attachments) > 1:
        ctx.reply("Only 1 image allowed")
        return

    async with ctx.typing():
        url = attachments[0].url
        player_info = await extract_player_info(gemini_client, url)
        if not player_info:
            ctx.reply("Internal Error")
            return

        name = player_info.get("name")
        clan = player_info.get("clan")

        if not name or not clan:
            ctx.reply("Internal Error")
            return

        deck = await search.find_deck(bot.browser, name, clan)

        if not deck:
            await ctx.reply("No deck found")
            return

        deck_image = await build_deck_image(deck)
        buffer = io.BytesIO()
        deck_image.save(buffer, format="PNG")
        buffer.seek(0)

    await ctx.reply(file=discord.File(buffer, filename="deck.png"))


bot.run(DISCORD_API_KEY)
