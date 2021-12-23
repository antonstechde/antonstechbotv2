import configparser
import subprocess
import os
from utils import utils


class Config:
    def __init__(self):
        self.__config_parser__ = configparser.ConfigParser(interpolation=None)
        self.__config_parser__.read(utils.get_project_dir() + "/config/config.ini")

        self.Version = None
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
        try:
            self.Version = subprocess.check_output(["git", "describe", "--tags", "--always"]).decode('ascii').strip()
        except:
            self.Version = "Unknown"

        try:
            bot_config = self.__config_parser__["BOT"]
            self.TOKEN = bot_config["TOKEN"]
            self.LOG_LEVEL = bot_config["LOG_SEVERITY"]
        except:
            try:
                os.getenv("DISCORD-TOKEN")
            except:
                raise Exception("No token found in config.ini or DISCORD-TOKEN env variable")
            try:
                os.getenv("LOG_LEVEL")
            except:
                raise Exception("No log level found in config.ini or LOG_LEVEL env variable")

        try:
            database_config = self.__config_parser__["DATABASE"]
            self.DATABASE_USER = database_config["USER"]
            self.DATABASE_PASSWORD = database_config["PASSWORD"]
            self.DATABASE_PORT = database_config["PORT"]
            self.DATABASE_HOST = database_config["HOST"]
            self.DATABASE_NAME = database_config["DATABASE"]
        except:
            try:
                self.DATABASE_USER = os.getenv("DATABASE_USER")
            except:
                raise Exception("No database user found in config.ini or DATABASE_USER env variable")
            try:
                self.DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
            except:
                raise Exception("No database password found in config.ini or DATABASE_PASSWORD env variable")
            try:
                self.DATABASE_PORT = os.getenv("DATABASE_PORT")
            except:
                raise Exception("No database port found in config.ini or DATABASE_PORT env variable")
            try:
                os.getenv("DATABASE_HOST")
            except:
                raise Exception("No database host found in config.ini or DATABASE_HOST env variable")
            try:
                os.getenv("DATABASE_NAME")
            except:
                raise Exception("No database name found in config.ini or DATABASE_NAME env variable")

        try:
            better_uptime_config = self.__config_parser__["BETTERUPTIME-INTEGRATION"]
            self.better_uptime_enabled = better_uptime_config["ENABLED"].lower() in ["true"]
            if self.better_uptime_enabled:
                self.better_uptime_url = better_uptime_config["WEBHOOK-URL"]
                self.better_uptime_times = better_uptime_config["HOW-OFTEN"]
        except:
            try:
                better_uptime_config = os.getenv("BETTERUPTIME_ENABLED")
                if better_uptime_config.lower() in ["true"]:
                    self.better_uptime_enabled = True
                    self.better_uptime_url = os.getenv("BETTERUPTIME_WEBHOOK_URL")
                    self.better_uptime_times = os.getenv("BETTERUPTIME_HOW_OFTEN")
                else:
                    self.better_uptime_enabled = False
            except:
                self.better_uptime_enabled = False

        self.memes_api_url = "https://meme-api.herokuapp.com/gimme"
