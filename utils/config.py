import configparser
from utils import utils


class Config:
    def __init__(self):
        self.__config_parser__ = configparser.ConfigParser(interpolation=None)
        self.__config_parser__.read(utils.get_project_dir() + "/config/config.ini")

        self.TOKEN = None
        self.LOG_LEVEL = None

        self.DATABASE_PORT = None
        self.DATABASE_HOST = None
        self.DATABASE_NAME = None
        self.DATABASE_USER = None
        self.DATABASE_PASSWORD = None

        self.better_uptime_enabled = None
        self.better_uptime_url = None
        self.better_uptime_times = None

        self.memes_api_url = None

        self.setup()

    def setup(self):
        bot_config = self.__config_parser__["BOT"]

        self.TOKEN = bot_config["TOKEN"]
        self.LOG_LEVEL = bot_config["LOG_SEVERITY"]

        database_config = self.__config_parser__["DATABASE"]

        self.DATABASE_USER = database_config["USER"]
        self.DATABASE_PASSWORD = database_config["PASSWORD"]
        self.DATABASE_PORT = database_config["PORT"]
        self.DATABASE_HOST = database_config["HOST"]
        self.DATABASE_NAME = database_config["DATABASE"]

        better_uptime_config = self.__config_parser__["BETTERUPTIME-INTEGRATION"]

        self.better_uptime_enabled = better_uptime_config["ENABLED"].lower() in ["true"]
        if self.better_uptime_enabled:
            self.better_uptime_url = better_uptime_config["WEBHOOK-URL"]
            self.better_uptime_times = better_uptime_config["HOW-OFTEN"]
        else:
            pass

        self.memes_api_url = "https://meme-api.herokuapp.com/gimme"
