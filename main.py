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

    SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

    @bot.event
    async def on_ready():
        server_names = [guild.name for guild in bot.guilds]
        final_server_names = ", ".join(server_names)
        config_string = f"""Information:
    - Logged in as {bot.user}
    - Bot running on Version {utils.CONFIG.Version}
    - discord-py-interaction version: {__version__}
    - Is in the following {str(len(bot.guilds))} servers:
        {final_server_names}
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
            utils.LOGGER.debug("Changed bot presence to 'your messages'")
            await asyncio.sleep(60)
            await bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.listening, name="to you talking in voice channels"))
            utils.LOGGER.debug("Changed bot presence to 'to you talking in voice channels'")

    for filename in os.listdir(utils.get_project_dir() + "/cogs/"):
        if filename.endswith(".py") and filename not in ["basicerror.py"]:
            utils.LOGGER.debug(f"Attempting to load cog {filename[:-3]}")
            bot.load_extension(f"cogs.{filename[:-3]}")

    bot.run(utils.CONFIG.TOKEN)


if __name__ == '__main__':
    main()
