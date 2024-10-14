import discord
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('sqlitedb\data.db')
c = conn.cursor()

class utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(description = 'Посмотреть свои или нет статки')
    async def stats(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        user_id = member.id
        c.execute(f'SELECT total_messages FROM message_data WHERE user_id={user_id}')
        total_messages = c.fetchall()
        c.execute(f'SELECT total_vctime FROM voicechat_data WHERE user_id={user_id}')
        total_vociechat = c.fetchall()
        embed=discord.Embed(title=f"", color=0x8294fe)
        embed.set_author(name=member.name, icon_url=member.avatar.url)
        embed.add_field(name="Сообщений отправлено: ", value=f"{total_messages[0][0]}", inline=True)
        embed.add_field(name="В голосовом канале просиженно: ", value=f"{round(total_vociechat[0][0] / 60, 1)} мин.", inline=True)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync(guild=None)

async def setup(bot):
    await bot.add_cog(utils(bot))