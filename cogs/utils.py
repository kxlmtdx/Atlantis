import discord
from discord.ext import commands
import sqlite3, datetime

class utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        bot = commands.Bot
        await bot.tree.sync()

async def setup(bot):
    await bot.add_cog(utils(bot))