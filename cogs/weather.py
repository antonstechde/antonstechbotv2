from datetime import datetime
from utils import utils
from discord.ext.commands import AutoShardedBot, Cog
from discord_slash import cog_ext, SlashContext
import requests
import discord


class Weather(Cog):
    def __init__(self, bot: AutoShardedBot):
        self.bot = bot
        # Yeah I know here is the plain Token :D
        self.api_key = "7d518678abe248fc7de360ba82f9375b"
        self.base_url = "https://api.openweathermap.org/data/2.5/weather?"
        utils.LOGGER.debug(f"Successfully loaded cog {self.__class__.__name__}")

    @cog_ext.cog_slash(name="weather", description="Lets you display the current Weather in a City",
                       options=[{
                           "name": "weather",
                           "description": "Please provide your City here",
                           "type": 3,
                           "required": "true"
                       }])
    async def _wetter_command(self, ctx: SlashContext, **kwargs):
        await ctx.defer(hidden=False)
        city = kwargs["weather"]
        try:
            complete_url = self.base_url + "appid=" + self.api_key + "&q=" + city + "&lang=en"
            response = requests.get(complete_url).json()
            if response["cod"] != "404":
                y = response["main"]
                current_temp = y["temp"]
                current_temp_celsius = str(round(current_temp - 273.15))
                pressure = y["pressure"]
                humidity = y["humidity"]
                feels_like = y["feels_like"]
                feels_like_celsius = str(round(feels_like - 273.15))
                z = response["weather"]
                symbol = z[0]["icon"]
                weather_desc = z[0]["description"]
                embed = discord.Embed(title=f"Weather in {city}",
                                      color=ctx.guild.me.top_role.color,
                                      timestamp=datetime.now(), )
                embed.add_field(name="Description", value=f"**{weather_desc}**", inline=False)
                embed.add_field(name="Temperature(C)", value=f"**{current_temp_celsius}°C**", inline=False)
                embed.add_field(name="Feels like(C)", value=f"**{feels_like_celsius}°C**",
                                inline=False)
                embed.add_field(name="Humidity(%)", value=f"**{humidity}%**", inline=False)
                embed.add_field(name="Air-Pressure(hPa)", value=f"**{pressure}hPa**", inline=False)
                embed.set_thumbnail(url="https://openweathermap.org/img/wn/" + symbol + ".png")
                embed.set_footer(text=f"Requested by {ctx.author.name}")
                await ctx.send(embed=embed)
            elif response["cod"] == "401":
                await ctx.send("The API Key of the Bot Owner is not Valid!")
            elif response["cod"] == "404":
                await ctx.send(f'City "{city}" was not found.')
            else:
                await ctx.send("Something went wrong")

        except:
            await ctx.send("Something went wrong")


def setup(client):
    client.add_cog(Weather(client))
