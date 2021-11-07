from discord.ext.commands import Cog, AutoShardedBot
from discord_slash import cog_ext, SlashContext

from utils import utils


class RoleReactions(Cog):
    def __init__(self, bot):
        self.bot: AutoShardedBot = bot
        utils.LOGGER.debug(f"Successfully loaded cog {self.__class__.__name__}")

    @cog_ext.cog_subcommand(base="role_reaction", name="create", description="Create a role reaction")
    async def role_reactions_create(self, ctx: SlashContext, **kwargs):
        print(str(kwargs))

    @cog_ext.cog_subcommand(base="role_reaction", name="delete", description="Delete a role reaction")
    async def role_reaction_delete(self, ctx:SlashContext, **kwargs):
        print(str(kwargs))


def setup(bot: AutoShardedBot):
    bot.add_cog(RoleReactions(bot))
