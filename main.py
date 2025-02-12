import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

GUILD_IDS = [1276905750232432660, 1339190286005309481]

@bot.event
async def on_ready():
    for guild_id in GUILD_IDS:
        guild = bot.get_guild(guild_id)
        if guild:
            try:
                await bot.tree.sync(guild=guild)
                print(f"Synced commands for {guild.name} ({guild.member_count} members) [{guild.id}]")
            except Exception as e:
                print(f"Failed to sync for {guild_id}: {e}")
        else:
            print(f"Bot is not in server {guild_id}, skipping sync.")

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over virgin monkeys"))

async def load_cogs():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            extension = f"commands.{filename[:-3]}"
            try:
                await bot.load_extension(extension)
                print(f"+ Loaded {filename[:-3]}")
            except Exception as e:
                print(f"- Failed to load {filename[:-3]}: {e}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())
