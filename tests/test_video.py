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
    with open(".cache/video_info.json", "w", encoding="utf-8") as f:
        import json

        json.dump(resp, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    import asyncio

    asyncio.run(test2())
