import discord
from discord.ext.commands import Cog, AutoShardedBot
from discord_slash import cog_ext, SlashContext
from utils import utils


class ServerUtils(Cog):
    """
    This class is supposed to contain a lot of server based stuff like "channel create/delete" or "user punish/unpunish"
    """

    def __init__(self, bot):
        self.bot: AutoShardedBot = bot
        utils.LOGGER.debug(f"Successfully loaded cog {self.__class__.__name__}")

    # @cog_ext.cog_subcommand(base="server", subcommand_group="user", name="punish", description="punishes a user")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="user", name="un-punish", description="un-punishes a user")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="user", name="add-role", description="adds a role to a user")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="user", name="remove-role", description="removes a role from a user")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="role", name="create", description="creates a role")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="role", name="edit", description="edits a role")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="role", name="delete", description="deletes a role")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="channel", name="create", description="creates a channel")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="channel", name="edit", description="edits a channel") # not sure about that one
    # @cog_ext.cog_subcommand(base="server", subcommand_group="channel", name="delete", description="deletes a channel")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="category", name="create", description="creates a category")
    # @cog_ext.cog_subcommand(base="server", subcommand_group="category", name="edit", description="edits a category") # not sure about that one
    # @cog_ext.cog_subcommand(base="server", subcommand_group="category", name="delete", description="deletes a category")



def setup(bot: AutoShardedBot):
    bot.add_cog(ServerUtils(bot))