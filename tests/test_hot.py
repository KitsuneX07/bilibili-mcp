from bilibili_api import hot
import pprint
import json


async def get_weekly_hot_videos():
	resp = await hot.get_hot_buzzwords(page_num=1, page_size=10)

	pprint.pprint(resp)
	with open(".cache/hot_buzzwords.json", "w", encoding="utf-8") as f:
		json.dump(resp, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
	import asyncio

	asyncio.run(get_weekly_hot_videos())
