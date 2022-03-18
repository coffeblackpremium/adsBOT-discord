import discord
import datetime
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='>', description="BOT da ADS Fasipe")

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Salve Salve", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    await ctx.send(embed=embed)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="Como Centralizar uma DIV", url="www.youtube.com/fabioakita"))
    print('Estou Pronto!')
bot.run(os.getenv('TOKEN'))