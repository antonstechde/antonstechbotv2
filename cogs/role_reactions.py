from discord.ext.commands import Cog, AutoShardedBot
from discord_slash import cog_ext, SlashContext

from utils import utils


class RoleReactions(Cog):
    def __init__(self, bot):
        self.bot: AutoShardedBot = bot
        utils.LOGGER.debug(f"Successfully loaded cog {self.__class__.__name__}")

    @cog_ext.cog_slash(name="role_reaction", description="manage role reactions", options=[{
        "name": "create",
        "description": "Create a role reaction",
        "type": 1,
        "required": "false",
        "options": [
            {
                "name": "channel",
                "description": "the id of the channel the message is in",
                "type": 7,
                "required": "true"
            },
            {
                "name": "message",
                "description": "the id of the message in the channel to react",
                "type": 3,
                "required": "true"
            },
            {
                "name": "emoji",
                "description": "the id of the emoji which should be used",
                "type": 3,
                "required": "true"
            },
            {
                "name": "role",
                "description": "the id of the role which should be given",
                "type": 8,
                "required": "true"
            }
        ]
    }])
    async def role_reactions(self, ctx: SlashContext, **kwargs):
        print(**kwargs)


def setup(bot: AutoShardedBot):
    bot.add_cog(RoleReactions(bot))
