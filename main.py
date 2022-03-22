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
    await bot.change_presence(activity=discord.Streaming(name="Como Centralizar uma DIV", url="www.youtube.com/fabioakita"))
    print(f'Estou Pronto! {bot.user} Está logado')

extensions = ['cogs.ClearCommands', 'cogs.MusicCommands']


if __name__ == '__main__':
    for ext in extensions:
        bot.load_extension(ext)
    bot.run(token)
