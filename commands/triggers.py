import discord
import json
import re
from discord.ext import commands

IGNORED_CHANNEL_IDS = [1339689938991448105, 1339688506137645167, 1339688534193209418, 1339688084954021998, 1339687676730937426]

class Triggers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_triggers(self):
        with open("database/triggers.json", "r", encoding="utf-8") as file:
            return json.load(file)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.channel.id in IGNORED_CHANNEL_IDS:
            return

        triggers = self.load_triggers()
        message_content = message.content.lower()
        
        for entry in triggers:
            if any(re.search(rf"\b{re.escape(trigger.lower())}\b", message_content) for trigger in entry["triggers"]):
                embed = discord.Embed(
                    title=entry.get("title", "Alert!"),
                    description=entry.get("description", ""),
                    color=discord.Color.brand_red()
                )

                for field in entry.get("fields", []):
                    embed.add_field(name=field["name"], value=field["value"], inline=False)

                if entry.get("image"):
                    embed.set_image(url=entry["image"])

                await message.reply(embed=embed)
                break

async def setup(bot):
    await bot.add_cog(Triggers(bot))
