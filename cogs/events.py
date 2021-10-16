import asyncio
from discord.ext.commands import Cog, Bot
from discord.ext import commands
from utils import config


class Events(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.mentions[0] == self.bot.user:
                await message.channel.send(f"Hey {message.author.mention} : ) \n "
                                           f"Discord does not want us to use text based Bots anymore so we switched to the new Slash Command System\n"
                                           f'Try it out by Typing "/" in this Channel :)')
        except IndexError:
            pass


def setup(bot):
    bot.add_cog(Events(bot))
