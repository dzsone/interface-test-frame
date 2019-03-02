"""
Log class. By reading the configuration file, define the log level, log file name, log format, and so on.
Generally import logger directly
from comm.Log import logger
logger.info('test log')
"""
import os,time, functools
import logging
from logging.handlers import TimedRotatingFileHandler
from comm.config import LOG_PATH, Config


class Logger(object):
    def __init__(self, logger_name='program name Autotest'):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        c = Config().get('log')
        self.log_file_name = time.strftime("%Y-%m-%d-%H-%M") + '_program name_interfaceTest.log'  # log file
        self.backup_count = c.get('backup') if c and c.get('backup') else 5  # retain logs num
        # Log output level
        self.console_output_level = c.get('console_level') if c and c.get('console_level') else 'WARNING'
        self.file_output_level = c.get('file_level') if c and c.get('file_level') else 'DEBUG'
        # Log output type
        pattern = c.get('pattern') if c and c.get('pattern') else '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.formatter = logging.Formatter(pattern)

    def get_logger(self):
        """Add a log handler to the logger and return it. If the logger already has a handle, return directly
         We add two handles here, one to output the log to the console and the other to the log file.
         The log levels of the two handles are different and can be set in the configuration file.
        """
        if not self.logger.handlers:  # Avoid duplicate logs
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            # Recreate a daily log file and keep up to backup_count
            file_handler = TimedRotatingFileHandler(filename=os.path.join(LOG_PATH, self.log_file_name),
                                                    when='D',
                                                    interval=1,
                                                    backupCount=self.backup_count,
                                                    delay=True,
                                                    encoding='utf-8'
                                                    )
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger

    def log_exception(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            logger = Logger().get_logger()
            try:
                fn(*args, **kwargs)
            except Exception as e:
                logger.exception("[Error in {}] msg: {}".format(__name__, str(e)))
                raise

        return wrapper

logger = Logger().get_logger()
