import pathlib
from utils.config import Config
from utils.logger import logger
from utils.logger.error_levels import Level, InfoLevel, ErrorLevel, WarningLevel, DebugLevel
from utils.dbConnector.Connector import Connector

CONFIG: Config
LOGGER: logger.Logger
dbCONNECTOR: Connector


def get_project_dir() -> str:
    """
    This is used to ensure that we will use the absolute path and not a relative path
    :return: Path of the project directory as a string
    """
    return str(pathlib.Path(__file__).parent.parent.absolute())


def run_checks():
    global CONFIG, LOGGER, dbCONNECTOR
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

    dbCONNECTOR = Connector(
        database=CONFIG.DATABASE_NAME,
        user=CONFIG.DATABASE_USER,
        password=CONFIG.DATABASE_PASSWORD,
        port=CONFIG.DATABASE_PORT,
        host=CONFIG.DATABASE_HOST
    )



