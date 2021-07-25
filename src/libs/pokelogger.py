from datetime import datetime, date
from enum import Enum

class LogLevel(Enum):
    INFO = 1, "INFO"
    WARN = 2, "WARN"
    ERR  = 3, "ERR"

class PokeLogger:
    """Class for simple Pokébot event logging.
    """
    def __init__(self, info_log: str, warn_log: str, error_log: str):
        """Constructor for logging into files

        Args:
            info_log (str): The path to the info level log file.
            warn_log (str): The path to the warning level log file.
            error_log (str): The path to the error level log file.
        """

        self.__logfiles = { 
            LogLevel.INFO : open(info_log,  "w+"),
            LogLevel.WARN : open(warn_log,  "w+"),
            LogLevel.ERR  : open(error_log, "w+")
        }

    def __del__(self):
        self.__logfiles[LogLevel.INFO].close()
        self.__logfiles[LogLevel.WARN].close()
        self.__logfiles[LogLevel.ERR].close()

    def log(self, msg: str, level : LogLevel = LogLevel.INFO):
        """Logs a message into the appropriate log file.

        Note: The default logging level will be LogLevel.INFO

        Args:
            msg (str): The message to be logged
            level (LogLevel): The logging level.
                A LogLevel.INFO level will log <msg> into self.__info.
                A LogLevel.WARN level will log <msg> into self.__warn.
                A LogLevel.ERR level will log <msg> into self.__err.

        """
        
        self.__logfiles[level].write(f"({datetime.now()}) [{LogLevel.INFO.value[1]}]: {msg}\n")
        self.__logfiles[level].flush()