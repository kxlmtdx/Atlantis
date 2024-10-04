import discord
from discord.ext import commands
import sqlite3


conn = sqlite3.connect('sqlitedb\data.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS command_usage
             (user_id INTEGER PRIMARY KEY, command_name TEXT, usage_count INTEGER)''')
conn.commit()

'''
    alter - изменить
    table - таблицу 
    linksauthor - название таблицы, которую менять 
    add - добавить column - колонку
    'description' - сюда будет подставлено название добавляемой колонки 
    'float' - тип добавляемой колонки - число с плавающей точкой
'''

#c.execute("alter table command_usage add column 'description' 'float'")
#conn.commit()

class init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        bot = commands.Bot
        await bot.tree.sync()
        print(f'{self.bot.user} Alive!')
        botactivity = discord.Activity(type=discord.ActivityType.watching,
                                   name="Христос Воскрес")
        await bot.change_presence(activity=botactivity, status=discord.Status.online)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        bot = commands.Bot
        if message.author == bot.user:
            return
        else:
            user_id = message.author.id
            c.execute("SELECT * FROM command_usage WHERE user_id=? AND command_name=?", (user_id, 'test1'))
            result = c.fetchone()

            if result is None:
                c.execute("INSERT INTO command_usage(user_id, command_name, usage_count) VALUES (?, ?, ?)", (user_id, 'test1', 1))
                conn.commit()
            else:
                c.execute("UPDATE command_usage SET usage_count=usage_count+1 WHERE user_id=? AND command_name=?", (user_id, 'test1'))
                conn.commit()

    @commands.hybrid_command()
    async def test1(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

async def setup(bot):
    await bot.add_cog(init(bot))