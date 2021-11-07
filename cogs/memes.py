from discord.ext.commands import AutoShardedBot, Cog
from discord_slash import cog_ext, SlashContext
from utils import utils
import discord
import requests


class Memes(Cog):
    def __init(self, bot: AutoShardedBot):
        self.bot = bot
        utils.LOGGER.debug(f"Successfully loaded cog {self.__class__.__name__}")

    @cog_ext.cog_slash(name="memes", description="Sends you a random Meme")
    async def memes_commands(self, ctx: SlashContext):
        await ctx.defer(hidden=False)
        response = requests.get(utils.CONFIG.memes_api_url)
        x = response.json()
        link = x["postLink"]
        reddit = x["subreddit"]
        titel = x["title"]
        img = x["url"]
        acc = x["author"]
        votes = x["ups"]
        embed = discord.Embed(url=link, title=titel)
        embed.set_image(url=img)
        embed.set_footer(text=f"Posted by u/{acc} in r/{reddit} with {votes} Upvotes")
        await ctx.send(embed=embed)


def setup(bot: AutoShardedBot):
    bot.add_cog(Memes(bot))
