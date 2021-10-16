from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
import os
import psutil
import platform
import time

uname = platform.uname()


class Status(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="status", description="Displays Information about the Bot")
    async def _status(self, ctx: SlashContext):
        pid = os.getpid()
        process = psutil.Process(pid)
        process.create_time()
        memoryuse = process.memory_full_info()
        await ctx.send(f"```prolog\n"
                       f"Discord Stuff:\n"
                       f"Servers: {len(self.bot.guilds)}\n"
                       f"Users: {len(set(self.bot.get_all_members()))}\n"
                       "-------\n"
                       f"Bot Technical:\n"
                       f"RAM-Usage: {memoryuse.rss / 1024000} MB \n"
                       f'Running Since: {time.strftime("%d.%m.%Y %H:%M", time.localtime(process.create_time()))}\n'
                       f"Websocket Latency: {round(self.bot.latency * 1000)}ms\n"
                       f"Shard Count: {len(list(self.bot.shards))}\n"
                       "-------\n"
                       f"System:\n"
                       f"CPU-Usage: {psutil.cpu_percent()}%\n"
                       f"RAM-Usage : {psutil.virtual_memory()[2]}%\n"
                       f"OS: {uname.system} {uname.version}\n"
                       f"System Architecture: {uname.machine}\n"
                       f"```")


def setup(bot: Bot):
    bot.add_cog(Status(bot))
