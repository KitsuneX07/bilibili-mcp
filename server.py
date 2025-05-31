import sys
import os
import asyncio

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from loguru import logger


sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.chdir(os.path.abspath(os.path.dirname(__file__)))

from mcp.server.fastmcp import FastMCP
from utils import setup_logger

mcp = FastMCP("bilibili-mcp")

from bilibili_api import Credential, video


async def test() -> None:
	# 实例化 Credential 类
	credential = Credential(sessdata=os.getenv("SESSDATA"), bili_jct=os.getenv("BILI_JCT"), buvid3=os.getenv("BUVID3"))
	# 实例化 Video 类
	v = video.Video(bvid="BV17V7pz9Eoe", credential=credential)
	info = await v.get_info()
	logger.info(f"{info}")
	# 给视频点赞
	await v.like(True)


@logger.catch
def main():
	# Setup logger
	setup_logger(log_dir=os.getenv("LOG_DIR", "logs"), console_log_level=os.getenv("CONSOLE_LOG_LEVEL", "INFO"), file_log_level=os.getenv("FILE_LOG_LEVEL", "DEBUG"))
	logger.info("Logger initialized.")
	# mcp.run()
	asyncio.run(test())


if __name__ == "__main__":
	main()
