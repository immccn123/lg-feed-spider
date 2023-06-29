'''
尽可能的抓取全部的犇犇，不回头。
'''

import json
import time

import requests

from db import models
from scripts.utils import calc_feed_hash

from tools.logger import HandleLog

logger = HandleLog()

while True:
    k = 1
    while True:
        logger.info(f'page {k}')
        k += 1
        is_created = 0
        try:
            r = requests.get(
              "https://www.luogu.com.cn/api/feed/list?page=" + str(k),
              headers={
                  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
              },
              timeout=12
            ).text
        except TimeoutError:
            logger.error('timeout when getting feeds.')
            continue
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
                    "time": feed["time"],
                    "content": feed["content"],
                    "grub_time": time.time(),
                },
            )
        time.sleep(1)
    time.sleep(5)
