import os
import sys

from dotenv import load_dotenv
from loguru import logger

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.chdir(os.path.abspath(os.path.dirname(__file__)))

from app import mcp
from app.favorite_list import *  # noqa: F403
from app.utils.logger import setup_logger
from app.video import *  # noqa: F403
from app.favorite_list import *  # noqa: F403


@logger.catch()
def main():
    # Setup logger
    setup_logger(log_dir=os.getenv("LOG_DIR", "logs"), console_log_level=os.getenv("CONSOLE_LOG_LEVEL", "INFO"), file_log_level=os.getenv("FILE_LOG_LEVEL", "DEBUG"))
    logger.info("Logger initialized.")
    mcp.run()


if __name__ == "__main__":
    main()
