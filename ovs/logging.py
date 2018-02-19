import sys
import logging
from flask import request

class Logger:
    def __init__(self, app):
        self.console_logger = logging.Logger(__name__)
        self.console_logger.setLevel(logging.DEBUG)

        # Set logging output format like 02/15/2018 23:20:45-INFO:
        stdout_logging_formatter = logging.Formatter(fmt='%(asctime)s-%(levelname)s:%(message)s', datefmt='%m/%d/%Y %H:%M:%S')

        # Log to stdout
        stdout_logging_handler = logging.StreamHandler(sys.stdout)
        stdout_logging_handler.setFormatter(stdout_logging_formatter)

        # Testing logging with two handlers
        self.console_logger.addHandler(stdout_logging_handler)
        self.console_logger.addHandler(logging.StreamHandler(sys.stderr))

    def __del__(self):
        # Close any handlers that need closing
        logging_handlers_copy = self.console_logger.handlers[:]
        for handler in logging_handlers_copy:
            handler.close()
            self.console_logger.removeHandler(handler)

    def debug(self, msg, *args, **kwargs):
        self.console_logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.console_logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.console_logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.console_logger.warning(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.console_logger.warning(msg, *args, **kwargs)

    def log(self, msg, *args, **kwargs):
        self.console_logger.warning(msg, *args, **kwargs)

class RequestFormatter(logging.Formatter):
    # flask.request data that can be logged defined here: http://flask.pocoo.org/docs/0.12/api/#flask.Request
    # Using flask.request global to add information about last request to record attribute dict for formatting
    def format(self, record):
        record.request_url = request.url #u'http://www.example.com/myapplication/π/page.html?x=y'
        record.request_args = request.args
        record.request_method = request.method # POST, GET, etc.

