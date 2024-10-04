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

    @commands.hybrid_command()
    async def xmas(self, ctx):
        now = datetime.datetime.today()
        NY = datetime.datetime(2021, 1, 1)
        d = NY-now
        mm, ss = divmod(d.seconds, 60)
        hh, mm = divmod(mm, 60)
        
        embed=discord.Embed()
        embed.add_field(name="До нового года осталось", value=f"{d.days} дней {hh} часа {mm} мин!", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(utils(bot))