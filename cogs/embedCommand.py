import discord
from discord.ext import commands, tasks
from main import bot


allowed_mentions = discord.AllowedMentions(everyone = True)

class EmbedCommand(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        channel_id = 956066188096585748
        channel = self.bot.get_channel(channel_id)
        role = discord.utils.get(channel.guild.roles, name="Membros")
        with open('botEmbed.txt', 'r') as f:
            text = f.read()
            embed = discord.Embed(name="farofa", title="Regras do Servidor", description=text, color=discord.Color.red())
            embed.set_author(name="farofa", url="https://github.com/coffeblackpremium", icon_url="https://img.wattpad.com/fff2e2cb66e0c768530730445400cb4115f4d82f/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f723178594933677569594b5a66773d3d2d35352e313636623037663239646136353237633439313138373332393631382e6a7067?s=fit&w=720&h=720")
            message = await channel.send(embed=embed)

        def check(reaction, user):
            return reaction.message == message and str(reaction) == '👍'

        reaction, user = await self.bot.wait_for('reaction_add', check=check)
        await user.add_roles(role)

def setup(bot):
    bot = bot.add_cog(EmbedCommand(bot))

        