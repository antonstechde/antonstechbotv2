import os
import pathlib
import sys
import traceback as tb_module
from datetime import datetime
from threading import Lock

from colorama import Style

from utils.logger.error_levels import Level


class Logger:
    def __init__(
        self,
        should_log_to_file: bool = False,
        only_print_over_and_including_severity=Level.InfoLevel(),
    ):
        self.__should_log_to_file__: bool = should_log_to_file
        self.__only_print_over_and_including_severity__ = only_print_over_and_including_severity

        sys.excepthook = self.custom_sys_except_hook

        self.__log_path__ = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + "/logs"
        self.__lock__ = Lock()

        if should_log_to_file:
            if not os.path.exists(self.__log_path__):
                os.mkdir(self.__log_path__)

            if os.path.exists(self.__log_path__ + "/bot.log.old"):
                os.remove(self.__log_path__ + "/bot.log.old")

            if os.path.exists(self.__log_path__ + "/bot.log"):
                os.rename(self.__log_path__ + "/bot.log", self.__log_path__ + "/bot.log.old")

    @staticmethod
    def __get_format__() -> str:
        return f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    def __print_message__(self, level: Level.Level, message):
        if level.severity_number >= self.__only_print_over_and_including_severity__.severity_number:
            print(
                f"{level.color}[{level.severity}] {self.__get_format__()}: {message}{Style.RESET_ALL}"
            )

        if self.__should_log_to_file__:
            with open(self.__log_path__ + "/bot.log", "a") as f:
                f.write(f"[{level.severity}] {self.__get_format__()}: {message}\n")

    def debug(self, message):
        with self.__lock__:
            self.__print_message__(level=Level.DebugLevel(), message=message)

    def info(self, message):
        with self.__lock__:
            self.__print_message__(level=Level.InfoLevel(), message=message)

    def warning(self, message):
        with self.__lock__:
            self.__print_message__(level=Level.WarningLevel(), message=message)

    def error(self, message):
        with self.__lock__:
            self.__print_message__(level=Level.ErrorLevel(), message=message)

    def custom_sys_except_hook(self, exctype, value, traceback):
        error = "".join(tb_module.format_exception(exctype, value, traceback))
        self.error(f"{exctype.__name__} was raised with error: {value}\n{error}")
        sys.__excepthook__(exctype, value, traceback)
