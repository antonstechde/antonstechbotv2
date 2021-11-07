from discord.ext.commands import AutoShardedBot, Cog
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_permission, SlashCommandPermissionType

from utils import utils


adminperms = {
    723220208772186156: [  # nur auf dem antonstech.de dc server
        create_permission(819476372867121173, SlashCommandPermissionType.ROLE, True),  # Programming-Stuff role
        create_permission(782026258921553933, SlashCommandPermissionType.ROLE, True),  # Admin role
    ]
}

class Exec(Cog):
    def __init__(self, bot: AutoShardedBot):
        self.bot = bot
        utils.LOGGER.debug(f"Successfully loaded cog {self.__class__.__name__}")

    @cog_ext.cog_slash(name="exec", description="Execute some command", options=[
        create_option(
            name="command",
            description="The command you want to run",
            option_type=3,
            required=True
        )
    ], default_permission=False, permissions=adminperms)
    async def exec_command(self, ctx: SlashContext, **kwargs):
        await ctx.defer(hidden=True)
        # still work in progress
        print(f"kwargs: {kwargs}")
        await ctx.send("done", hidden=True)


def setup(bot: AutoShardedBot):
    bot.add_cog(Exec(bot))
