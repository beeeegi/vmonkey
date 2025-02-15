import discord
import os
import datetime
from discord.ext import commands

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_filename = f"logs/session_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    def log_event(self, event):
        timestamp = datetime.datetime.now().strftime("[%d/%m/%Y | %H:%M:%S]")
        with open(self.log_filename, "a", encoding="utf-8") as log_file:
            log_file.write(f"{timestamp} {event}\n")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild and not message.author.bot:
            self.log_event(f"@{message.author.name} ({message.author.id}) -> {message.content}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.guild and not before.author.bot:
            self.log_event(f"@{before.author.name} ({before.author.id}) EDITED MESSAGE: '{before.content}' -> '{after.content}'")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild and not message.author.bot:
            self.log_event(f"@{message.author.name} ({message.author.id}) DELETED MESSAGE: '{message.content}'")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.guild and not user.bot:
            self.log_event(f"@{user.name} ({user.id}) ADDED REACTION {reaction.emoji} TO MESSAGE: '{reaction.message.content}'")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.message.guild and not user.bot:
            self.log_event(f"@{user.name} ({user.id}) REMOVED REACTION {reaction.emoji} FROM MESSAGE: '{reaction.message.content}'")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.log_event(f"@{member.name} ({member.id}) JOINED THE SERVER")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        self.log_event(f"@{member.name} ({member.id}) LEFT THE SERVER")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        self.log_event(f"@{user.name} ({user.id}) BANNED FROM SERVER")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        self.log_event(f"@{user.name} ({user.id}) UNBANNED FROM SERVER")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            self.log_event(f"@{before.name} ({before.id}) CHANGED NICKNAME: '{before.nick}' -> '{after.nick}'")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            self.log_event(f"@{member.name} ({member.id}) JOINED VC")
        elif before.channel is not None and after.channel is None:
            self.log_event(f"@{member.name} ({member.id}) LEFT VC")

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        self.log_event(f"CHANNEL CREATED: {channel.name} ({channel.id})")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        self.log_event(f"CHANNEL DELETED: {channel.name} ({channel.id})")

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        self.log_event(f"CHANNEL UPDATED: {before.name} -> {after.name}")

async def setup(bot):
    await bot.add_cog(Logging(bot))
