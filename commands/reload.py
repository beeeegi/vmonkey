import discord
from discord.ext import commands

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="reload", description="Reloads all the loaded commands without resetting the bot [OWNER ONLY]")
    @commands.is_owner()
    async def reload(self, ctx):
        msg = await ctx.reply("🛠 Reloading commands. It may take some time...")

        try:
            for extension in list(self.bot.extensions):
                await self.bot.reload_extension(extension)            
            try:
                synced = await self.bot.tree.sync()
                await msg.edit(content=f"✅ Syned and reloaded `{len(synced)}` commands")
            except Exception as sync_error:
                await msg.edit(content=f"❌ Error: `{sync_error}`") 
        except Exception as e:
            await msg.edit(content=f"❌ Error: `{e}`") 

async def setup(bot):
    await bot.add_cog(Reload(bot))
