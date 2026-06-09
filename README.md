# Clash Royale Deck Bot

This bot uses ```RoyaleAPI``` and official ```Clash Royale API``` to find a player by their nickname and clan. Then it outputs the deck they played last, which is likely to be the deck they are playing right now.

I am using Python with Playwright to search by nickname/clan on RoyaleAPI since the official API only lets you find a player by their tag.
The bot expects two API keys in your environment variables:

```CR_KEY``` - Clash Royale API key.

```DISCORD_KEY``` - Discord bot token.

Additionaly I'm using Pillow to create the image of the deck that the bot sends to the chat.

All the required dependencies can be installed with:
```bash
pip3 install -r requirements.txt
```

Run the bot:
```bash
cd src/
python3 bot.py
```

When the bot is on, the command to search for a deck is:
```
>d <nickname> <clan>
```
If either nickname or clan have multiple words in them, they have to be wrapped in speech marks.
Clan is optional but if not given, only users with no clan will be searched
