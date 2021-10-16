from discord.ext.commands import Bot, Cog
from discord.ext import commands, tasks
import requests
from utils import utils
import asyncio


class Betteruptime(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


# So this checks if it should use the Betteruptime Function
if utils.CONFIG.better_uptime_enabled == "true" or utils.CONFIG.better_uptime_enabled == "TRUE":

    @tasks.loop(minutes=int(utils.CONFIG.better_uptime_times))
    async def send_request():
        requests.get(utils.CONFIG.better_uptime_url)

    send_request.start()

else:
    pass


def setup(bot):
    bot.add_cog(Betteruptime(bot))
