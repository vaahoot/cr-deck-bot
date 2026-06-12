import discord
from google import genai

from config import DISCORD_API_KEY, GEMINI_API_KEY
from CRBot import CRBot, save_preferences
from helper import print_error, print_info

if not DISCORD_API_KEY:
    raise ValueError("API key not found")

browser = None

intents = discord.Intents.default()
intents.message_content = True

gemini_client = genai.Client(api_key=GEMINI_API_KEY)
bot = CRBot(command_prefix="!", intents=intents, gemini_client=gemini_client)


# Command to find player's deck by name and clan
@bot.command()
async def d(ctx):
    if not bot.browser:
        print_error("No browser is initialized")
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

    await bot.search_by_info(name, clan, ctx.message)


# Command to find player's deck by an image
@bot.command()
async def i(ctx):
    if not bot.browser:
        print_error("No browser is initialized")
        await ctx.reply("Internal Error")
        return

    await bot.search_by_image(ctx.message)


# Command to set the channel in which !i is not needed for the bot to start searching by screenshot.
@bot.command()
async def image_channel(ctx, state):
    guild_id = str(ctx.guild.id)
    channels = bot.preferences.setdefault(guild_id, [])

    if state.lower() == "on":
        if ctx.channel.id in channels:
            await ctx.reply(f"{ctx.channel.name} is already an image channel")
            return

        bot.preferences[guild_id].append(ctx.channel.id)
        save_preferences(bot.preferences)
        print_info(
            f"Channel: {ctx.channel.name}, ID: {ctx.channel.id} was set as an image channels list"
        )
        await ctx.reply(f"Channel {ctx.channel.name} set as image channel")

    elif state.lower() == "off":
        if not channels:
            await ctx.reply(f"Channel {ctx.channel.name} wasn't an image channel")
            return

        if ctx.channel.id not in channels:
            await ctx.reply(f"Channel {ctx.channel.name} wasn't an image channel")
            return

        bot.preferences[guild_id].remove(ctx.channel.id)
        save_preferences(bot.preferences)
        print_info(
            f"Channel: {ctx.channel.name}, ID: {ctx.channel.id} was removed from image channels list"
        )
        await ctx.reply(f"Channel {ctx.channel.name} is no longer an image channel")

    else:
        await ctx.reply("Invalid state")


bot.run(DISCORD_API_KEY)
