import sys
import os
import asyncio

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from loguru import logger

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.chdir(os.path.abspath(os.path.dirname(__file__)))
from app import mcp

from app.utils import setup_logger, CredentialManager


from bilibili_api import video


async def test() -> None:
	# 实例化 Credential 类
	credential = CredentialManager.get_instance()
	# 实例化 Video 类
	v = video.Video(bvid="BV14y7sz3E4x", credential=credential)
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
