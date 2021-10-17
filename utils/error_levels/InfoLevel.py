from colorama import Fore
from .Level import Level


class InfoLevel(Level):
    def __init__(self):
        super().__init__()
        self.severity = "INFO"
        self.color = Fore.CYAN
        self.severity_number = 1
