import discord
from discord.ext import commands
import yt_dlp
import youtube_dl
import asyncio
import os
from main import bot

yt_dlp.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
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

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

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

class MusicCommands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'O BOT de Música está online')

    @commands.command()
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send(f'{ctx.message.author.name} Não está conectado em um canal de voz')
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command()
    async def play(self, ctx, url:str):
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client
            voice_client = ctx.message.guild.voice_client
            channel = ctx.message.author.voice.channel

            async with ctx.typing():
                filename = await YTDLSource.from_url(url, loop=bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename))
            await ctx.send(f'**Você está ouvindo: {filename} **')
        except:
            await ctx.send(f"{ctx.author.mention}, o Bot não está conectado em nenhum canal de Voz.")
        if voice_client.is_playing():
                os.remove(filename)
        await channel.disconnect()
        
    @commands.command()
    async def leave(self, ctx):
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if not voice is None:
            if voice.is_connected():
                await voice.disconnect()
            else:
                await ctx.send(f'{ctx.author.mention} O BOT não está conectado em nenhuma sala!')
        else:
            await ctx.send(f'{ctx.author.mention} O BOT não está conectado em nenhuma sala!')
    @commands.command()
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
            await ctx.send(f'{ctx.author.mention}, pausou a Musica')
        else:
            await ctx.send("O Bot não está tocando nenhuma música no momento")

    @commands.command()
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
            await ctx.send(f'{ctx.author.mention}, Voltou com a música ')
        else:
            await ctx.send("O Bot não está tocando nenhuma música agora. Utilize o comando: play + (url) para iniciar uma musica")

    @commands.command()
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send(f"{ctx.author.mention}, O BOT não está tocando nenhuma musica no momento")

def setup(bot):
    bot.add_cog(MusicCommands(bot))
