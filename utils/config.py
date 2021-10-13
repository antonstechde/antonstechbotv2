import configparser
from utils import utils

TOKEN = None


def setup():
    global TOKEN
    config = configparser.ConfigParser()
    config.read(utils.get_project_dir() + "/config/config.ini")

    bot_config = config["BOT"]

    TOKEN = bot_config["TOKEN"]
