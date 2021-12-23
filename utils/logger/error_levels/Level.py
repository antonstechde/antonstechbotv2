from colorama import Fore


class Level:
    def __init__(self):
        self.color = None
        self.severity = None
        self.severity_number = -1


class InfoLevel(Level):
    def __init__(self):
        super().__init__()
        self.severity = "INFO"
        self.color = Fore.CYAN
        self.severity_number = 1


class WarningLevel(Level):
    def __init__(self):
        super().__init__()
        self.severity = "Warning"
        self.color = Fore.YELLOW
        self.severity_number = 2


class ErrorLevel(Level):
    def __init__(self):
        super().__init__()
        self.severity = "ERROR"
        self.color = Fore.RED
        self.severity_number = 3


class DebugLevel(Level):
    def __init__(self):
        super().__init__()
        self.severity = "DEBUG"
        self.color = Fore.LIGHTWHITE_EX
        self.severity_number = 0
