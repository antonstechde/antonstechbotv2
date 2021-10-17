from discord import Guild
from discord.ext.commands import Cog, Bot
from discord.ext import commands
from utils import utils


class Events(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        utils.LOGGER.debug(f"Successfully loaded cog {self.__class__.__name__}")

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.mentions[0] == self.bot.user:
                await message.channel.send(f"Hey {message.author.mention} : ) \n "
                                           f"Discord does not want us to use text based Bots anymore so we switched to the new Slash Command System\n"
                                           f'Try it out by Typing "/" in this Channel :)')
        except IndexError:
            pass

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        utils.LOGGER.error(f"Discord.py error: \nEvent: {event}\n*args: {args}\n**kwargs: {kwargs}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        utils.LOGGER.info(f"Joined guild '{guild.name}' ({guild.id})")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        utils.LOGGER.info(f"Left guild '{guild.name}' ({guild.id})")


def setup(bot):
    bot.add_cog(Events(bot))
