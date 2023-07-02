"""
从老版本json格式转为数据库格式。
"""

import datetime
import json

from db import get_connection, models
from scripts.utils import calc_feed_hash
from tools.logger import HandleLog

from .utils import print_process

logger = HandleLog()


def detect_start_point(feed, l: int, r: int):
    """二分找数据起始点"""
    global main_database
    logger.info("detecting start point.")
    while r - l > 20:
        mid = (l + r) // 2
        # print(mid)
        feed_hash = calc_feed_hash(
            int(feed[mid]["user"].split("#")[1]),
            feed[mid]["time"],
            feed[mid]["content"],
        )

        res = models.Feed.select().where(models.Feed.hash == feed_hash)
        # print(list(res))

        if not list(res):
            r = mid
        else:
            l = mid

    for i in range(l, r):
        feed_hash = calc_feed_hash(
            int(feed[i]["user"].split("#")[1]), feed[i]["time"], feed[i]["content"]
        )
        res = models.Feed.select().where(models.Feed.hash == feed_hash)
        if list(res):
            logger.info(f"detected start point {i}.")
            return i

    if l == 0:
        logger.info("start insert from 0")
        return 0

    logger.error("cannot find start point,file may be exported.")


def mainloop():
    """主要逻辑，见上"""
    global main_database
    main_database = get_connection()
    with open(
        input("                    filename (json format):"), "r", encoding="utf-8"
    ) as read_stream:
        origin_file = json.load(read_stream)

    # start_point = input('[leave blank if no]start from x-th message:')
    cnt = detect_start_point(origin_file, 0, len(origin_file))

    for feed in origin_file:
        cnt += 1
        print_process(cnt, len(origin_file))
        stime = feed["time"]
        user = feed["user"].split("#")[0]
        uid = int(feed["user"].split("#")[1])
        content = feed["content"]
        feed_hash = calc_feed_hash(uid, stime, content)
        models.Feed.get_or_create(
            hash=feed_hash,
            defaults={
                "user_id": uid,
                "user_color": "Unknown",
                "username": user,
                "time": datetime.datetime.fromtimestamp(stime),
                "content": content,
                "grub_time": datetime.datetime.now(),
            },
        )
        if cnt % 1000 == 0:
            main_database.commit()
    main_database.commit()
    main_database.close()
    print()
