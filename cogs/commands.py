import os

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Cog
from discord_slash import SlashContext, cog_ext

from config.adminconfig import get_admin_permissions
from utils import utils


def ist_gepinnt(message):
    return not message.pinned


class Commands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        utils.LOGGER.debug(f"Successfully loaded cog {self.__class__.__name__}")

    @cog_ext.cog_slash(name="invite", description="Lets you invite the Bot")
    async def _bot_invite(self, ctx: SlashContext):
        embed = discord.Embed()
        embed.set_author(
            name="Click me :D",
            url=discord.utils.oauth_url(
                self.bot.user.id,
                permissions=discord.Permissions(8),
                guild=ctx.guild,
                scopes=["bot", "applications.commands"],
            ),
        )
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="vote", description="Here you can find a link to vote for our bot <3")
    async def _vote(self, ctx: SlashContext):
        embed = discord.Embed()
        embed.set_author(
            name="Currently we only have a few Votes but you can vote for us here :D",
            url="https://top.gg/bot/744218316167708773/vote",
        )
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(
        name="shutdown",
        description="Shuts down the bot",
        default_permission=False,
        permissions=get_admin_permissions(),
    )
    async def _shutdown(self, ctx: SlashContext):
        os.system("git pull")
        await ctx.send("Shutting down...")
        await self.bot.logout()

    @cog_ext.cog_slash(name="clear", description="Clears the chat")
    @commands.has_permissions(manage_messages=True)
    async def clear_command(self, ctx: SlashContext, amount: int = 7):
        try:
            amount = int(amount)
            await ctx.channel.purge(limit=amount + 1, check=ist_gepinnt)
            await ctx.send(f"{amount} Messages were deleted by {ctx.author} :)", delete_after=7)
        except TypeError:
            await ctx.send("Invalid amount of messages to delete")
            return


def setup(bot: Bot):
    bot.add_cog(Commands(bot))
