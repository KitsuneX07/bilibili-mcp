import sys
import os
from loguru import logger

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.chdir(os.path.abspath(os.path.dirname(__file__)))

from mcp.server.fastmcp import FastMCP
from utils import load_config, setup_logger

mcp = FastMCP("bilibili-mcp")


def main():
	load_config()
    # Setup logger
	setup_logger(
        log_dir=os.getenv("LOG_DIR", "logs"),
        console_log_level=os.getenv("CONSOLE_LOG_LEVEL", "INFO"),
        file_log_level=os.getenv("FILE_LOG_LEVEL", "DEBUG"),
    )
	logger.info("Logger initialized.")
	# mcp.run()


if __name__ == "__main__":
	main()
