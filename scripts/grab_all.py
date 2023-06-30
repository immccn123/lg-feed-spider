"""
尽可能的抓取全部的犇犇，不回头。
"""

import json
import time

import datetime
import requests

from db import models
from scripts.utils import calc_feed_hash

from tools.logger import HandleLog

logger = HandleLog()

while True:
    k = 1
    while True:
        logger.info(f"[Grab_all] Page {k}")
        try:
            r = requests.get(
                "https://www.luogu.com.cn/api/feed/list?page=" + str(k),
                headers={
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
                },
                timeout=12,
            ).text
        except TimeoutError:
            logger.error("[Grab_all] Timed out when getting feeds.")
            continue
        k += 1
        r: list = json.loads(r)["feeds"]["result"]
        if len(r) == 0:
            break
        for feed in r:
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
