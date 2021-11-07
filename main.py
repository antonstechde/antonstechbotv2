import asyncio
import os

import discord
from discord import Intents
from discord.ext.commands import AutoShardedBot
from discord_slash import SlashCommand, __version__

from utils import utils


def main():
    utils.run_checks()

    # Note that command_prefix is a required but essentially unused parameter.
    # Setting help_command=False ensures that discord.py does not create a !help command. <--- Doesn't work lol
    # Enabling self_bot ensures that the bot does not try and parse messages that start with "!".
    bot = AutoShardedBot(command_prefix="!", self_bot=True, intents=Intents.all())
    bot.remove_command("help")

    SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True, debug_guild=761304285798989896)

    @bot.event
    async def on_ready():
        server_string = '        \n'.join([guild.name for guild in bot.guilds])
        config_string = f"""Information:
    - Logged in as {bot.user}
    - discord-py-interaction version: {__version__}
    - Is in servers:
        {server_string}
        """

        utils.LOGGER.info(config_string)

        bot.loop.create_task(status_task())

    async def status_task():
        while True:
            await bot.change_presence(activity=discord.Game("https://git.io/techbotv2"),
                                      status=discord.Status.online)
            utils.LOGGER.debug("Changed bot presence to 'https://git.io/techbotv2'")
            await asyncio.sleep(60)
            await bot.change_presence(
                activity=discord.Game("on " + str(len(bot.guilds)) + " Servers"))
            utils.LOGGER.debug("Changed bot presence to 'on " + str(len(bot.guilds)) + " Servers'")
            await asyncio.sleep(60)
            await bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name="your Messages"))
            await asyncio.sleep(60)
            utils.LOGGER.debug("Changed bot presence to 'your messages'")

    for file in os.listdir(utils.get_project_dir() + "/cogs/"):
        if os.path.isdir(utils.get_project_dir() + "/cogs/" + file):
            continue

        utils.LOGGER.debug(f"Attempting to load cog {file[:-3]}")
        bot.load_extension(f"cogs.{file[:-3]}")

    bot.run(utils.CONFIG.TOKEN)


if __name__ == '__main__':
    main()
