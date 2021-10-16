from discord.ext.commands import AutoShardedBot, Cog
from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_choice

from utils import utils


class PrivateChannel(Cog):
    def __init(self, bot: AutoShardedBot):
        self.bot = bot

    @cog_ext.cog_slash(name="private_channel", description="Some private channel command", options=[
        create_choice(name="create", value="create"),
        create_choice(name="delete", value="delete")
    ])
    async def private_channel(self, ctx: SlashContext, **kwargs):
        # still work in progress
        print(f"kwargs: {kwargs}")
        await ctx.send("test")


def setup(bot: AutoShardedBot):
    bot.add_cog(PrivateChannel(bot))
