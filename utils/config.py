import configparser
from utils import utils


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

        self.setup()

    def setup(self):
        bot_config = self.__config_parser__["BOT"]

        self.TOKEN = bot_config["TOKEN"]

        for item in self.__config_parser__.items():
            print(item)

        # database_config = self.__config_parser__["DATABASE"]
        #
        # self.DATABASE_USER = database_config["USER"]
        # self.DATABASE_PASSWORD = database_config["PASSWORD"]
        # self.DATABASE_PORT = database_config["PORT"]
        # self.DATABASE_HOST = database_config["HOST"]
        # self.DATABASE_NAME = database_config["DATABASE"]


