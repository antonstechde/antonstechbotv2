from discord.ext.commands import AutoShardedBot, Cog
from discord_slash import cog_ext, SlashContext
import datetime
from utils import utils
import discord
import requests


class Minecraft(Cog):
    def __init(self, bot: AutoShardedBot):
        self.bot = bot
        utils.LOGGER.debug(f"Successfully loaded cog {self.__class__.__name__}")

    @cog_ext.cog_slash(name="minecraft",
                       description="Lets you look up Minecraft Skins and Servers", options=[
            {
                "name": "skin",
                "description": "Lets you look up a Skin",
                "type": 3,
                "required": "false"
            },

            {
                "name": "server",
                "description": "lets you look up a Server",
                "type": 3,
                "required": "false"
            }

        ])
    async def minecraft_commands(self, ctx: SlashContext, **kwargs):
        await ctx.defer(hidden=False)
        try:
            playername = kwargs["skin"]
            uuid = "https://api.mojang.com/users/profiles/minecraft/" + playername
            response = requests.get(uuid)
            x = response.json()
            playeruuid = x["id"]
            head = "https://crafatar.com/avatars/"
            body = "https://crafatar.com/renders/body/"
            embed = discord.Embed(title="Minecraft Skin von " + playername)
            embed.set_thumbnail(url=head + playeruuid + "?size=50")
            embed.set_image(url=body + playeruuid + "?size=512")
            embed.set_author(name="Skin Download", url="https://minotar.net/download/" + playername)
            await ctx.send(embed=embed)
        except:
            try:
                servername = kwargs["server"]
                base_url = "https://api.mcsrvstat.us/2/"
                complete_url = base_url + servername
                response = requests.get(complete_url).json()
                status = response["online"]
                embed = discord.Embed(title=f'Minecraft Server Stats for "{servername}"')
                if status is True:
                    modt = response["motd"]["clean"][0]
                    playercount = response["players"]
                    spieleronline = playercount["online"]
                    slots = playercount["max"]
                    embed.add_field(name="Description", value=f"{modt}")
                    embed.add_field(name="Players", value=f"{spieleronline} / {slots}")
                    try:
                        version = response["version"]
                        software = response["software"]
                        embed.add_field(name="Version", value=f"{software} {version}")
                    except:
                        pass
                    try:
                        version = response["version"]
                        embed.add_field(name="Version", value=version)
                    except:
                        embed.add_field(name="Version", value="Unknown")
                    try:
                        mods = response["mods"]["names"]
                        if mods != "":
                            embed.set_author(name="Modlist",
                                             url='https://mcsrvstat.us/server/' + servername)
                            embed.add_field(name="Modlist", value="See link above")
                        else:
                            pass
                    except:
                        pass
                    embed.set_thumbnail(url="https://api.mcsrvstat.us/icon/" + servername)
                    if response["debug"]["cachetime"] != 0:
                        unix_time = response["debug"]["cachetime"]
                        time = datetime.datetime.fromtimestamp(int(unix_time)).strftime("%H:%M:%S")
                        embed.set_footer(text=f"The Results are from {time}")
                    else:
                        pass
                    if response["players"]["online"] < 10:
                        try:
                            playernames = str(response["players"]["list"])
                            characters_to_remove = "'[]"
                            for character in characters_to_remove:
                                playernames = playernames.replace(character, "")
                            embed.add_field(name="Playernames:", value=playernames)
                        except:
                            pass
                    else:
                        pass
                    await ctx.send(embed=embed)
                else:
                    embed.set_footer(text="The Server is not Online")
                    await ctx.send(embed=embed)
            except KeyError:
                await ctx.send(f'{ctx.author.mention} Invalid Option! Choose "skin" or "server"')
            except:
                await ctx.send("Something went wrong!")


def setup(bot: AutoShardedBot):
    bot.add_cog(Minecraft(bot))
