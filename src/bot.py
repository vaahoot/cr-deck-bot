import discord

import search
import io
from deck import build_deck_image
from config import DISCORD_API_KEY
from CRBot import CRBot

if not DISCORD_API_KEY:
    raise ValueError("API key not found")

browser = None

intents = discord.Intents.default()
intents.message_content = True

bot = CRBot(command_prefix=">", intents=intents)

@bot.command()
async def d(ctx, name, clan=None):
    if not bot.browser:
        await ctx.reply("ERROR: No browser is initialized")
        return

    print(f"[INFO] Searching for: {name}, Clan: {clan if clan else "No clan"}")

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
