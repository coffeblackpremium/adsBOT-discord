import discord
import datetime
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import youtube_dl
from pygame import mixer

load_dotenv('.env')

bot = commands.Bot(command_prefix='>', description="BOT da ADS Fasipe")


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

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
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send(f'{ctx.message.author.name} Não está conectado em um canal de voz')
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command()
async def play(ctx, url:str):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_client = ctx.message.guild.voice_client
        channel = ctx.message.author.voice.channel

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename))
        await ctx.send(f'**Você está ouvindo: {filename} **')
        if voice_client.is_playing():
            os.remove(filename)
            await channel.disconnect()
    except:
        await ctx.send(f"{ctx.message.author.name}, o Bot não está conectado em nenhum canal de Voz.")
    
@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice is None:
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send(f'{ctx.author.mention} O BOT não está conectado em nenhuma sala!')
    else:
        await ctx.send(f'{ctx.author.mention} O BOT não está conectado em nenhuma sala!')
@bot.command()
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("O Bot não está tocando nenhuma música no momento")

@bot.command()
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("O Bot não está tocando nenhuma música agora. Utilize o comando: play + (url) para iniciar uma musica")

@bot.command()
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send(f"{ctx.author.mention}, O BOT não está tocando nenhuma musica no momento")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name="Como Centralizar uma DIV", url="www.youtube.com/fabioakita"))
    print(f'Estou Pronto! {bot.user} Está logado')

bot.run(os.getenv("TOKEN"))