import logging
import os
import sys
from logging import StreamHandler
from logging.handlers import RotatingFileHandler, SysLogHandler

from pythonjsonlogger import jsonlogger


def setup_logging():
    """
    Setting up structured and human-readable logging:
    - ConsoleHandler (human-readable format) for local development.
    - JSON StreamHandler for Docker/syslog.
    - RotatingFileHandler for saving logs to disk.
    - SysLogHandler (optional) for centralized collection.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 1) Readable console log
    console_formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z"
    )
    ch = StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(console_formatter)
    logger.addHandler(ch)

    # 2) JSON log for Docker/syslog
    json_handler = StreamHandler(sys.stdout)
    json_handler.setLevel(logging.INFO)
    json_formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime) %(name) %(levelname) %(message)',
        timestamp=True
    )
    json_handler.setFormatter(json_formatter)
    logger.addHandler(json_handler)

    # 3) Log files rotation
    log_path = os.getenv("LOG_FILE_PATH", "/app/logs/giftbot.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    fh = RotatingFileHandler(
        filename=log_path,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    fh.setLevel(logging.INFO)
    fh.setFormatter(console_formatter)
    logger.addHandler(fh)

    # 4) Syslog (optional)
    syslog_host = os.getenv("SYSLOG_HOST")
    if syslog_host:
        sys_handler = SysLogHandler(
            address=(syslog_host, int(os.getenv("SYSLOG_PORT", 514)))
        )
        sys_handler.setLevel(logging.INFO)
        sys_handler.setFormatter(console_formatter)
        logger.addHandler(sys_handler)

    return logger
