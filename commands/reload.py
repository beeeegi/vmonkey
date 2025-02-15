import discord
from discord.ext import commands
from discord import app_commands

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reload", description="Reloads all the loaded commands without resetting the bot [OWNER ONLY]")
    async def reload(self, interaction: discord.Interaction):
        if not await self.bot.is_owner(interaction.user):
            return await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)

        msg = await interaction.response.send_message("Reloading commands. It may take some time...", ephemeral=True)

        try:
            for extension in list(self.bot.extensions):
                await self.bot.reload_extension(extension)

            try:
                synced = await self.bot.tree.sync()
                await interaction.edit_original_response(content=f"Synced and reloaded `{len(synced)}` commands")
            except Exception as sync_error:
                await interaction.edit_original_response(content=f"❌ Error while syncing: `{sync_error}`")
        except Exception as e:
            await interaction.edit_original_response(content=f"❌ Error while reloading: `{e}`")

async def setup(bot):
    await bot.add_cog(Reload(bot))
