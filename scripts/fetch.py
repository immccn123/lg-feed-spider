"""
用于轮询更新犇犇（实时的）。
"""
import datetime
import json
import time
import requests

from db import get_connection, models
from scripts.utils import calc_feed_hash

from tools.logger import HandleLog

logger = HandleLog()

main_database = get_connection()


def mainloop():
    """主要逻辑，见上"""
    while True:
        k = 1
        while True:
            logger.info(f"Current Page: {k}")
            is_created = 0
            cnt = 0
            try:
                result_get = requests.get(
                    "https://www.luogu.com.cn/api/feed/list?page=" + str(k),
                    headers={
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
                    },
                    timeout=10,
                ).text
            except TimeoutError:
                logger.error("Timed out when getting feeds. Retrying.")
                continue
            k += 1
            result_get: list = json.loads(result_get)["feeds"]["result"]
            if len(result_get) == 0:
                break
            for feed in result_get:
                feed_hash = calc_feed_hash(
                    feed["user"]["uid"], feed["time"], feed["content"]
                )
                _, is_created = models.Feed.get_or_create(
                    hash=feed_hash,
                    defaults={
                        "user_id": feed["user"]["uid"],
                        "user_color": feed["user"]["color"],
                        "username": feed["user"]["name"],
                        "time": datetime.datetime.fromtimestamp(feed["time"]),
                        "content": feed["content"],
                        "grub_time": datetime.datetime.now(),
                    },
                )
                cnt += is_created
            time.sleep(1)
            if cnt != 20:
                logger.info("Page End")
                break
        time.sleep(5)


if __name__ == "__main__":
    mainloop()
