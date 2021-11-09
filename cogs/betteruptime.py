from discord.ext.commands import Bot, Cog
from discord.ext import commands, tasks
import requests
from utils import utils
import asyncio


class Betteruptime(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.run()
        utils.LOGGER.debug(f"Successfully loaded cog {self.__class__.__name__}")

    @staticmethod
    def run():
        # So this checks if it should use the Betteruptime Function
        if utils.CONFIG.better_uptime_enabled:

            @tasks.loop(minutes=int(utils.CONFIG.better_uptime_times))
            async def send_request():
                requests.get(utils.CONFIG.better_uptime_url)
                utils.LOGGER.debug("Successfully sent Heartbeat Webhook")

            send_request.start()


def setup(bot):
    bot.add_cog(Betteruptime(bot))
