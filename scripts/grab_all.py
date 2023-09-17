"""
尽可能的抓取全部的犇犇，不回头。
"""

import datetime
import time

from db import models
from scripts.utils import calc_feed_hash, grab
from tools.logger import HandleLog

logger = HandleLog()


def mainloop():
    """主要逻辑，见上"""
    progress_file = open("progress", "r", encoding="utf-8")
    k = int(progress_file.read().strip())
    progress_file.close()
    while True:
        logger.info(f"[Grab_all] Page {k}")
        result_get: list = grab(k)
        k += 1
        progress_file = open("progress", "w", encoding="utf-8")
        progress_file.write(str(k))
        progress_file.close()
        if len(result_get) == 0:
            k = 1
            continue
        for feed in result_get:
            feed_hash = calc_feed_hash(
                feed["user"]["uid"], feed["time"], feed["content"]
            )
            models.Feed.get_or_create(
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
        time.sleep(5)
