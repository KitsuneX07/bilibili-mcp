import os
import sys

from bilibili_api import favorite_list
from dotenv import load_dotenv
from loguru import logger

from app.utils import CredentialManager

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(os.path.join(os.path.dirname(__file__), ".."))


cre = CredentialManager.get_instance()
uid = os.getenv("DEDEUSERID")


async def test_create_favorite_list():
	resp = await favorite_list.create_video_favorite_list(title="Test Favorite List", introduction="This is a test favorite list.", private=True, credential=cre)
	id = resp.get("id")
	logger.info(f"Created favorite list with ID: {id}")


async def test_get_favorite_list():
	resp = await favorite_list.get_video_favorite_list(uid=uid, credential=cre)
	logger.info(f"Retrieved favorite list: {resp}")
	with open(".cache/favorite_list.json", "w", encoding="utf-8") as f:
		import json

		json.dump(resp, f, ensure_ascii=False, indent=4)


async def test_delete_favorite_list():
	resp = await favorite_list.delete_video_favorite_list(media_ids=[3533640315], credential=cre)
	logger.info(f"Deleted favorite list response: {resp}")


if __name__ == "__main__":
	import asyncio

	asyncio.run(test_delete_favorite_list())
