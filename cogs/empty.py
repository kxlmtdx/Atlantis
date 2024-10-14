import discord
from discord.ext import commands

class utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#It's empty here for now, would you like to fix that?

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync(guild=None)

    async def setup(bot):
        await bot.add_cog(utils(bot))