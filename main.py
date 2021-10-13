from discord import Client, Intents, Embed
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext
from utils import utils
from utils import config
import os

# Note that command_prefix is a required but essentially unused paramater.
# Setting help_command=False ensures that discord.py does not create a !help command.
# Enabling self_bot ensures that the bot does not try and parse messages that start with "!".
bot = Bot(command_prefix="!", self_bot=True, intents=Intents.default())
bot.remove_command("help")

slash = SlashCommand(bot)

config.setup()


@slash.slash(name="test")
async def test(ctx: SlashContext):
    embed = Embed(title="Embed test")
    await ctx.send(embed=embed)


for file in os.listdir(utils.get_project_dir() + "/cogs/"):
    bot.load_extension(f"cogs/{file[:-3]}")


bot.run(config.TOKEN)
