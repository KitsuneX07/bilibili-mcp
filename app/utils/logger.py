import os
from sys import stderr

from loguru import logger

console_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>[{process.name}:{process.id}]</cyan> | <level>{message}</level>"


def setup_logger(log_dir: str = "logs", console_log_level: str = "INFO", file_log_level: str = "DEBUG"):
    logger.remove()  # Remove the default logger

    logger.add(
        stderr,
        level=console_log_level,
        format=console_format,
        colorize=True,
        enqueue=True,  # Crucial for MP
        backtrace=True,
        diagnose=True,
    )

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger.add(
        log_dir + "/log_{time:YYYY-MM-DD-HH-mm-ss}.log",
        level=file_log_level,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level:<8} [{process.name}:{process.id}] {message}",
        enqueue=True,  # Crucial for MP
        backtrace=True,
        diagnose=True,
    )
