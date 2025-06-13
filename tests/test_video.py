import os
import sys

from dotenv import load_dotenv
from loguru import logger


load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(os.path.join(os.path.dirname(__file__), ".."))


async def test1():
	from app.video.video import get_cid

	resp = await get_cid("BV1s87qzuE3U", 0)
	logger.info(resp)


async def test2():
	from app.video.video import get_info

	resp = await get_info("BV1s87qzuE3U")
	with open(".cache/video_info.json", "w", encoding="utf-8") as f:
		import json

		json.dump(resp, f, ensure_ascii=False, indent=4)


async def test3():
	from app.video.video import get_download_url

	resp = await get_download_url("BV1XotKeKEoD", 0)
	with open(".cache/video_download_url.txt", "w", encoding="utf-8") as f:
		for item in resp:
			f.write(f"{item}\n")


async def test4():
	from app.video.video import get_ai_conclusion

	resp = await get_ai_conclusion("BV1XotKeKEoD", 0)
	print(resp)


if __name__ == "__main__":
	import asyncio

	asyncio.run(test2())
