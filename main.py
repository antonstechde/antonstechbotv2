import asyncio
import os

import discord
from discord import Intents
from discord.ext.commands import AutoShardedBot
from discord_slash import SlashCommand, __version__

from utils import utils


def main():

    # Note that command_prefix is a required but essentially unused parameter.
    # Setting help_command=False ensures that discord.py does not create a !help command. <--- Doesn't work lol
    # Enabling self_bot ensures that the bot does not try and parse messages that start with "!".
    bot = AutoShardedBot(command_prefix="!", self_bot=True, intents=Intents.all())
    bot.remove_command("help")

    slash = SlashCommand(bot, sync_commands=False, sync_on_cog_reload=False, debug_guild=761304285798989896)

    utils.run_checks()

    @bot.event
    async def on_ready():
        print(f"""You are logged in as {bot.user} via discord-py-interactions version {__version__}
The bot is running on {len(list(bot.shards))} shards
The bot is in following {str(len(bot.guilds))} servers:""")
        for guild in bot.guilds:
            print("- " + str(guild.name))
        bot.loop.create_task(status_task())

    async def status_task():
        while True:
            await bot.change_presence(activity=discord.Game("https://git.io/techbotv2"),
                                      status=discord.Status.online)
            await asyncio.sleep(60)
            await bot.change_presence(
                activity=discord.Game("on " + str(len(bot.guilds)) + " Servers"))
            await asyncio.sleep(60)
            await bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name="your Messages"))
            await asyncio.sleep(60)

    for file in os.listdir(utils.get_project_dir() + "/cogs/"):
        if os.path.isdir(utils.get_project_dir() + "/cogs/" + file):
            continue

        bot.load_extension(f"cogs.{file[:-3]}")

    bot.run(utils.CONFIG.TOKEN)


if __name__ == '__main__':
    main()
