from bilibili_api import video_zone
import pprint

if __name__ == "__main__":
	import asyncio

	async def test():
		resp = video_zone.get_zone_info_by_name("鬼畜")
		pprint.pprint(resp)

	asyncio.run(test())
