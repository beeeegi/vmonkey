import discord
import json
from datetime import datetime, timedelta
from discord import app_commands
from discord.ext import commands

class Time(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_timezones(self):
        try:
            with open("database/timezones.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_timezones(self, data):
        with open("database/timezones.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    # Command to get a user's time
    @app_commands.command(name="time", description="Shows the current time for the user")
    async def time(self, interaction: discord.Interaction, user: discord.User):
        timezones = self.load_timezones()
        user_id = str(user.id)

        if user_id not in timezones:
            await interaction.response.send_message(
                f"{user.mention} has no time zone set, please contact the bot developer.",
                ephemeral=True
            )
            return

        user_timezone = timezones[user_id]

        try:
            if "GMT" in user_timezone:
                sign = 1 if "+" in user_timezone else -1
                offset_str = user_timezone.split("GMT")[1]
                
                if ":" in offset_str:
                    hours, minutes = map(int, offset_str.split(":"))
                    offset = timedelta(hours=hours * sign, minutes=minutes * sign)
                else:
                    offset = timedelta(hours=int(offset_str) * sign)

                user_time = datetime.utcnow() + offset
                user_time_str = user_time.strftime("%I:%M %p")

            embed = discord.Embed(
                title=f"{user.display_name}'s Time",
                description=f"{user_time_str}",
                color=discord.Color.brand_red()
            )
            embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
            
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"Error processing time zone for {user.mention}.", ephemeral=True)
            print(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(Time(bot))
