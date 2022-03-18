import discord
import datetime
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('.env')

bot = commands.Bot(command_prefix='>', description="BOT da ADS Fasipe")

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Salve Salve", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    await ctx.send(embed=embed)

@bot.command()
async def clear(ctx, limit:int):
    await ctx.channel.purge(limit=limit+1)
    await ctx.send(f'O {ctx.author.mention} Apagou {limit} Mensagens.')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="Como Centralizar uma DIV", url="www.youtube.com/fabioakita"))
    print(f'Estou Pronto! {bot.user} Está logado')

bot.run(os.getenv("TOKEN"))