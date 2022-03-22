import discord
from discord.ext import commands

class ClearCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Clear Esta Funcionando!')

    @commands.command()
    async def clear(self, ctx, limit:int):
        await ctx.channel.purge(limit=limit+1)
        await ctx.send(f'O {ctx.author.mention} Apagou {limit} Mensagens')

def setup(bot):
    bot.add_cog(ClearCommands(bot))