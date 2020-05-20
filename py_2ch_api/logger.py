import logging.config
import os
from datetime import datetime


class LOG_LEVEL:
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0


class Logger:
    def __init__(
        self,
        service: str = None,
        log_folder: str = "logs",
        logger_level: str = "DEBUG",
        log_to_file: bool = False,
    ):

        if not service:
            raise AttributeError("service name is not defined")

        try:
            os.mkdir(log_folder)
        except FileExistsError:
            pass

        self.service = service
        self.log_to_file = log_to_file
        self.logger_level = logger_level
        self.logger_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "std_format": {
                    "format": "{asctime} - {levelname} - {message}",
                    "style": "{",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "std_format",
                },
                "file": {
                    "class": "logging.FileHandler",
                    "filename": f"{log_folder}/log-{datetime.now().strftime('%Y-%m-%d')}.log",
                    "mode": "a",
                    "formatter": "std_format",
                },
            },
            "loggers": {
                self.service: {
                    "level": logger_level,
                    "handlers": ["console", "file"]
                    if self.log_to_file
                    else ["console"],
                }
            },
        }

        logging.config.dictConfig(self.logger_config)

        self.logger = logging.getLogger(self.service)

    def log(
        self,
        message: str = None,
        level: int = LOG_LEVEL.DEBUG,
        special: bool = False,
        special_char: str = "#",
        *args,
        **kwargs,
    ):
        """
        GENERIC LOG METHOD
        """
        if special:
            self.logger.log(
                level=level,
                msg=f"{special_char * 25} | {message} | {special_char * 25}",
                *args,
                **kwargs,
            )
        else:
            self.logger.log(level=level, msg=message, *args, **kwargs)

    def info(
        self,
        message: str = None,
        special: bool = False,
        special_char: str = "#",
        *args,
        **kwargs,
    ):
        self.log(
            message,
            LOG_LEVEL.INFO,
            special=special,
            special_char=special_char,
            *args,
            **kwargs,
        )

    def debug(
        self,
        message: str = None,
        special: bool = False,
        special_char: str = "#",
        *args,
        **kwargs,
    ):
        self.log(
            message,
            LOG_LEVEL.DEBUG,
            special=special,
            special_char=special_char,
            *args,
            **kwargs,
        )

    def error(
        self,
        message: str = None,
        special: bool = False,
        special_char: str = "#",
        exc_info: bool = True,
        *args,
        **kwargs,
    ):
        self.log(
            message,
            LOG_LEVEL.ERROR,
            special=special,
            special_char=special_char,
            exc_info=exc_info,
            *args,
            **kwargs,
        )

    def critical(
        self,
        message: str = None,
        special: bool = False,
        special_char: str = "#",
        exc_info: bool = True,
        *args,
        **kwargs,
    ):
        self.log(
            message,
            LOG_LEVEL.CRITICAL,
            special=special,
            special_char=special_char,
            exc_info=exc_info,
            *args,
            **kwargs,
        )
