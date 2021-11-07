from discord.ext.commands import AutoShardedBot, Cog
from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
import psycopg2
from utils import utils

utils.LOGGER.debug(f"Trying to connect to the database at {utils.CONFIG.DATABASE_HOST}")
# Connect do database
utils.LOGGER.debug(f"Successfully connected to {utils.CONFIG.DATABASE_HOST}")


class PrivateChannel(Cog):
    def __init(self, bot: AutoShardedBot):
        self.bot = bot
        utils.LOGGER.debug(f"Successfully loaded cog {self.__class__.__name__}")

    @cog_ext.cog_slash(name="channel", description="Allows you to create Private Channels :)", options=[
        {
            "name": "create",
            "description": "Create a private channel",
            "type": 3,
            "required": "false"
        },

        {
            "name": "delete",
            "description": "Delete your own private Channel",
            "type": 3,
            "required": "false"
        },

        {
            "name": "allow",
            "description": "Allow a Person to join in your Channel",
            "type": 6,
            "required": "false"
        },

        {
            "name": "deny",
            "description": "Disallow a Person from joining your Channel",
            "type": 6,
            "required": "false"
        },

        {
            "name": "remove",
            "description": "(ADMIN ONLY) remove a Channel",
            "type": 6,
            "required": "false"
        },

        {
            "name": "on or off",
            "description": "(ADMIN ONLY) lets you turn on or off the whole function",
            "type": 3,
            "required": "false"
        },

        {
            "name": "category",
            "description": "(ADMIN ONLY) lets you set the Category where Channels should be created",
            "type": 3,
            "required": "false"
        }

    ])
    async def private_channel(self, ctx: SlashContext, **kwargs):
        if "create" in kwargs:
            print("...")
        elif "delete" in kwargs:
            print("...")
        elif "allow" in kwargs:
            print("...")
        elif "deny" in kwargs:
            print("...")
        elif "remove" in kwargs:
            print(...)
        elif "on/off" in kwargs:
            print("...")
        elif "category" in kwargs:
            print("...")
        else:
            await ctx.send("Invalid Option")


def setup(bot: AutoShardedBot):
    bot.add_cog(PrivateChannel(bot))
