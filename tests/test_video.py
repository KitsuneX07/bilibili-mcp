import os
import sys

from dotenv import load_dotenv
from loguru import logger


load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(os.path.join(os.path.dirname(__file__), ".."))


async def test2():
    from app.video.video import get_video_info

    resp = await get_video_info("BV1WWMuzTE37")
    part_cid_map = {page.part: page.cid for page in resp.pages}
    print(part_cid_map)
    with open(".cache/video_info.json", "w", encoding="utf-8") as f:
        import json

        json.dump(resp, f, ensure_ascii=False, indent=4)


async def test3():
    from app.video.video import get_cid_by_part_name

    cid = await get_cid_by_part_name("BV1WWMuzTE37", "赛前评论")
    print(cid)
    cid = await get_cid_by_part_name("BV1WWMuzTE37", "第一局")
    print(cid)
    cid = await get_cid_by_part_name("BV1WWMuzTE37", "赛后采")
    print(cid)

async def test4():
    from app.video.download import download_video_best_quality
    return await download_video_best_quality(
        bvid="BV1j1421Q7Wj",
    )

if __name__ == "__main__":
    import asyncio

    asyncio.run(test4())
