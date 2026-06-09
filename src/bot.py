import discord

import search
from config import DISCORD_API_KEY
from Speedwagon import Speedwagon

if not DISCORD_API_KEY:
    raise ValueError("API key not found")

browser = None

intents = discord.Intents.default()
intents.message_content = True

bot = Speedwagon(command_prefix=">", intents=intents)

@bot.command()
async def d(ctx, name, clan):
    deck = await search.find_deck(bot.browser, name, clan)

    if deck:
        await ctx.send(", ".join(deck))
    else:
        await ctx.send("No deck found")


bot.run(DISCORD_API_KEY)
