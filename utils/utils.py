import pathlib

import discord_slash

from .config import Config
from .logger import logger
from .logger.error_levels import Level, InfoLevel, ErrorLevel, WarningLevel, DebugLevel
from .dbConnector.Connector import Connector
import discord

CONFIG: Config
LOGGER: logger.Logger
DB_CONNECTOR: Connector


def get_project_dir() -> str:
    """
    This is used to ensure that we will use the absolute path and not a relative path
    :return: Path of the project directory as a string
    """
    return str(pathlib.Path(__file__).parent.parent.absolute())


def return_embed(ctx: discord_slash.SlashContext, name, content, color: discord.Color) -> discord.Embed:
    embed = discord.Embed(color=color, timestamp=ctx.created_at)
    embed.add_field(name=name, value=content, inline=False)
    return embed


async def get_emoji(guild: discord.guild.Guild, input_to_get):
    emoji: discord.Emoji = await guild.fetch_emoji(input_to_get)

    return emoji


def run_checks():
    global CONFIG, LOGGER, DB_CONNECTOR
    CONFIG = Config()

    error_level: Level.Level

    if CONFIG.LOG_LEVEL == "DEBUG":
        error_level = DebugLevel.DebugLevel()
    elif CONFIG.LOG_LEVEL == "INFO":
        error_level = InfoLevel.InfoLevel()
    elif CONFIG.LOG_LEVEL == "WARNING":
        error_level = WarningLevel.WarningLevel()
    elif CONFIG.LOG_LEVEL == "ERROR":
        error_level = ErrorLevel.ErrorLevel()
    else:
        print("Invalid log error level defined. Defaulting to INFO")
        error_level = InfoLevel.InfoLevel()

    LOGGER = logger.Logger(should_log_to_file=True, only_print_over_and_including_severity=error_level)

    DB_CONNECTOR = Connector(
        database=CONFIG.DATABASE_NAME,
        user=CONFIG.DATABASE_USER,
        password=CONFIG.DATABASE_PASSWORD,
        port=CONFIG.DATABASE_PORT,
        host=CONFIG.DATABASE_HOST
    )

    DB_CONNECTOR.connect()



