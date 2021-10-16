import configparser
from utils import utils
from configparser import *

class Config:
    def __init__(self):
        self.__config_parser__ = configparser.ConfigParser()
        self.__config_parser__.read(utils.get_project_dir() + "/config/config.ini")

        self.TOKEN = None
        self.DATABASE_PORT = None
        self.DATABASE_HOST = None
        self.DATABASE_NAME = None
        self.DATABASE_USER = None
        self.DATABASE_PASSWORD = None

        self.better_uptime_enabled = None
        self.better_uptime_url = None
        self.better_uptime_times = None

        self.setup()

    def setup(self):
        bot_config = self.__config_parser__["BOT"]

        self.TOKEN = bot_config["TOKEN"]

        database_config = self.__config_parser__["DATABASE"]

        self.DATABASE_USER = database_config["USER"]
        self.DATABASE_PASSWORD = database_config["PASSWORD"]
        self.DATABASE_PORT = database_config["PORT"]
        self.DATABASE_HOST = database_config["HOST"]
        self.DATABASE_NAME = database_config["DATABASE"]

        better_uptime_config = self.__config_parser__["BETTERUPTIME-INTEGRATION"]

        self.better_uptime_enabled = better_uptime_config["ENABLED"]
        if self.better_uptime_enabled == "true":
            self.better_uptime_url = better_uptime_config["WEBHOOK-URL"]
            self.better_uptime_times = better_uptime_config["HOW-OFTEN"]
        else:
            pass
