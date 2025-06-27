import logging
import os
import sys
from logging import StreamHandler
from logging.handlers import RotatingFileHandler, SysLogHandler

from pythonjsonlogger import jsonlogger

from src.config.config_service import ConfigService


def setup_logging() -> logging.Logger:
    """
    Configure logging for both local development and production:
      - DEBUG mode: human-readable console output + local file logs.
      - Production: structured JSON logs to stdout + rotating file logs.
      - Optional SysLogHandler (if SYSLOG_HOST is set).
    """
    logger = logging.getLogger()
    debug_mode = os.getenv("DEBUG", "False") == 'True'
    logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)

    # 1) Remove any pre-existing handlers
    for h in list(logger.handlers):
        logger.removeHandler(h)

    # 2) File handler — path depends on environment
    #    локально будет ./logs/giftbot.log, в контейнере — /app/logs/giftbot.log
    config = ConfigService()
    default_path = config.logging_file_path

    fh = RotatingFileHandler(
        filename=default_path,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    fh.setLevel(logging.INFO)
    text_fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z"
    )
    fh.setFormatter(text_fmt)
    logger.addHandler(fh)

    # 3) Console or JSON to stdout
    if debug_mode:
        # human-readable console output
        ch = StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(text_fmt)
        logger.addHandler(ch)
    else:
        # structured JSON for Docker/syslog
        jh = StreamHandler(sys.stdout)
        jh.setLevel(logging.INFO)
        jf = jsonlogger.JsonFormatter(
            fmt="%(asctime) %(name) %(levelname) %(message)",
            timestamp=True
        )
        jh.setFormatter(jf)
        logger.addHandler(jh)

    # 4) Optional SysLogHandler
    syslog_host = os.getenv("SYSLOG_HOST")
    if syslog_host:
        try:
            sh = SysLogHandler(address=(syslog_host, os.getenv("SYSLOG_PORT", 514)))
            sh.ident = "giftbot"
            sh.setLevel(logging.INFO)
            sh.setFormatter(text_fmt)
            logger.addHandler(sh)
        except Exception as e:
            logger.warning("Could not set up SysLogHandler (%s:%s): %s",
                           syslog_host, os.getenv("SYSLOG_PORT", 514), e)

    return logger
