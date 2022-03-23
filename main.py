import discord
import datetime
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('.env')
token = os.getenv("TOKEN")

bot = commands.Bot(command_prefix='>', description="BOT da ADS Fasipe")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Centralizando uma Div"))


if __name__ == '__main__':
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
    bot.run(token)
