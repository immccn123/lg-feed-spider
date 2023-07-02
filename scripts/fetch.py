"""
用于轮询更新犇犇（实时的）。
"""
import datetime
import time

from db import models
from scripts.utils import calc_feed_hash,grab

from tools.logger import HandleLog

def mainloop():
    '''主要逻辑，见上'''
    logger = HandleLog()
    while True:
        k = 1
        while True:
            logger.info(f"Current Page: {k}")
            is_created = 0
            cnt = 0
            result_get: list = grab(k)
            k += 1
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
                logger.info(f"{feed['user']['name']}#{feed['user']['uid']}")
                cnt += is_created
            time.sleep(1)
            if cnt == 0:
                logger.info("Page End")
                break
        time.sleep(5)

if __name__ == '__main__':
    mainloop()
