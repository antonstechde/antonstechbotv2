import discord
from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from utils import utils


class Commands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        utils.LOGGER.debug(f"Successfully loaded cog {self.__class__.__name__}")

    @cog_ext.cog_slash(name="about")
    async def _about(self, ctx: SlashContext):
        embed = Embed(title="Embed Test")
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="invite", description="Lets you invite the Bot")
    async def _bot_invite(self, ctx: SlashContext):
        embed = discord.Embed()
        embed.set_author(name="Press the Link to invite the bot",
                         url=discord.utils.oauth_url(self.bot.user.id, permissions=discord.Permissions(8),
                                                     guild=ctx.guild, scopes=["bot", "applications.commands"]))
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="vote", description="Here you can find a link to vote for our bot <3")
    async def _vote(self, ctx: SlashContext):
        embed = discord.Embed()
        embed.set_author(name=f"Currently we only have a few Votes but you can vote for us here :D",
                         url="https://top.gg/bot/744218316167708773/vote")
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Commands(bot))
