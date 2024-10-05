import discord
from discord.ext import commands
import asyncio, os, json
import sqlite3, time

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='da', intents=intents, help_command=None)

with open('config.json') as f:
    data = json.load(f)
    token = data['token']

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f'[loaded] {filename}')

async def main():
    await load()
    await bot.start(token)
    await bot.tree.sync()

asyncio.run(main())