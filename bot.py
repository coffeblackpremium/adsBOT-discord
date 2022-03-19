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
async def creditos(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Salve familia. Este BOT é pertencente a Atlética Virais", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
    await ctx.send(embed=embed)

@bot.command()
async def virais(ctx):
    await ctx.send(f'Essa atlética é do balaco baco  😎')

@bot.command()
async def clear(ctx, limit:int):
    await ctx.channel.purge(limit=limit+1)
    await ctx.send(f'O {ctx.author.mention} Apagou {limit} Mensagens.')

@bot.command()
async def play(ctx, url:str):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Sala de estudo 1')
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    await voiceChannel.connect()
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="Como Centralizar uma DIV", url="www.youtube.com/fabioakita"))
    print(f'Estou Pronto! {bot.user} Está logado')

bot.run(os.getenv("TOKEN"))