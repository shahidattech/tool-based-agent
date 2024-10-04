import logging
from app.core.config import settings

ALL_LOG_LEVELS = {
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG
}

LOG_GROUP_NAME = settings.LOG_GROUP_NAME
LOG_STREAM_NAME = settings.LOG_STREAM_NAME
LOG_LEVEL = settings.LOG_LEVEL


class Logger:
    def __init__(self):
        self.formatstring = '%(asctime)s - %(name)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s'
        self.logger = logging.getLogger(LOG_GROUP_NAME)
        self.logger.setLevel(ALL_LOG_LEVELS[LOG_LEVEL])


    def __init_console_handler(self):
        detailed_formatter = logging.Formatter(self.formatstring)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(detailed_formatter)
        return console_handler
    
    def __init_stdout_handler(self):
        detailed_formatter = logging.Formatter(self.formatstring)
        stdout_handler = logging.StreamHandler()
        stdout_handler.setFormatter(detailed_formatter)
        return stdout_handler

    def get_logger(self):
        for logger in settings.LOGGERS:
            if logger == "console":
                console_handler =  self.logger.addHandler(self.__init_console_handler())
            elif logger == "stdout":
                 self.logger.addHandler(self.__init_stdout_handler())
            elif logger == "cloudwatch":
                pass
        return self.logger

logger: Logger = Logger().get_logger()
    