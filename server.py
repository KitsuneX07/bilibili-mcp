import sys
import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from loguru import logger

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.chdir(os.path.abspath(os.path.dirname(__file__)))
from app import mcp

from app.utils import setup_logger
from app.video import *

@logger.catch()
def main():
	# Setup logger
	setup_logger(log_dir=os.getenv("LOG_DIR", "logs"), console_log_level=os.getenv("CONSOLE_LOG_LEVEL", "INFO"), file_log_level=os.getenv("FILE_LOG_LEVEL", "DEBUG"))
	logger.info("Logger initialized.")
	mcp.run()


if __name__ == "__main__":
	main()
