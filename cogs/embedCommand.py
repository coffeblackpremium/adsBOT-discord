import discord
from discord.ext import commands, tasks
from main import bot

allowed_mentions = discord.AllowedMentions(everyone = True)


class EmbedCommand(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'O Embed está funcionado')

    
    @commands.command()
    async def __Regraszs(self, ctx):
        with open('botEmbed.txt', 'r') as f:
            content = f.read()
            embed = discord.Embed(name="farofa", title="Regras do Servidor", description=content, color=discord.Color.red())
            embed.set_author(name="farofa", url="https://www.instagram.com/joaont17/", icon_url=f"https://anime-girls-holding-programming-books.netlify.app/static/Kurumizawa_Satanichia_CSharp-78908f5f9c0a1d159c4a8551f1e66fb8.png")
            await ctx.send(embed=embed)
        await ctx.send(f'@everyone')

def setup(bot):
    bot = bot.add_cog(EmbedCommand(bot))

        