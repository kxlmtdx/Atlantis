import discord
from discord.ext import commands
import sqlite3, time
from datetime import datetime


conn = sqlite3.connect('sqlitedb\data.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS message_data
             (user_id INTEGER, server_id INTEGER, total_messages INTEGER, PRIMARY KEY (user_id, server_id))''')

c.execute('''CREATE TABLE IF NOT EXISTS voicechat_data
             (user_id INTEGER, server_id INTEGER, total_vctime INTEGER, PRIMARY KEY (user_id, server_id))''')
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

class VoiceTracker:
    voice_session_times = {}

class init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync(guild=None)
        print(f'{self.bot.user} Alive!')
        botactivity = discord.Activity(type=discord.ActivityType.watching,
                                   name="Hello?")
        await self.bot.change_presence(activity=botactivity, status=discord.Status.online)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        bot = commands.Bot
        if message.author == bot.user:
            return
        else:
            user_id = message.author.id
            server_id = message.guild.id
            c.execute("SELECT * FROM message_data WHERE user_id=? AND server_id=?", (user_id, server_id))
            result = c.fetchone()

            if result is None:
                c.execute("INSERT INTO message_data(user_id, server_id, total_messages) VALUES (?, ?, 1)", (user_id, server_id))
                conn.commit()
            else:
                c.execute("UPDATE message_data SET total_messages=total_messages+1 WHERE user_id=? AND server_id=?", (user_id, server_id))
                conn.commit()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            VoiceTracker.voice_session_times[member.id] = time.time()
        elif before.channel is not None and after.channel is None:
            user_id = member.id
            server_id = member.guild.id
            if user_id in VoiceTracker.voice_session_times:
                session_time = time.time() - VoiceTracker.voice_session_times[user_id]
                del VoiceTracker.voice_session_times[user_id]
                try:
                    c.execute("SELECT * FROM voicechat_data WHERE user_id=? AND server_id=?", (user_id, server_id))
                    result = c.fetchone()
                    if result is None:
                        c.execute("INSERT INTO voicechat_data(user_id, server_id, total_vctime) VALUES (?, ?, ?)", (user_id, server_id, int(session_time)))
                    else:
                        c.execute("UPDATE voicechat_data SET total_vctime=total_vctime+? WHERE user_id=? AND server_id=?", (int(session_time), user_id, server_id))
                    conn.commit()
                except sqlite3.Error as e:
                    print(f"Error writing to database: {e}")

async def setup(bot):
    await bot.add_cog(init(bot))