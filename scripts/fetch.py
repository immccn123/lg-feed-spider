'''
用于轮询更新犇犇（实时的）。
'''

import datetime
import json
import time
import requests

from db import getConnection, models
from scripts.utils import calc_feed_hash

from tools.logger import HandleLog

logger = HandleLog()

db = getConnection()

try:
    while True:
        k = 1
        while True:
            print("page", k)
            is_created = 0
            cnt = 0
            try:
                r = requests.get(
                  "https://www.luogu.com.cn/api/feed/list?page=" + str(k),
                  headers={
                      "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
                  },
                  timeout=10
              ).text
            except TimeoutError:
                logger.error('timeout when getting feeds.')
                continue
            k += 1
            r: list = json.loads(r)["feeds"]["result"]
            if len(r) == 0:
                break
            for feed in r:
                feed_hash = calc_feed_hash(
                    feed["user"]["uid"], feed["time"], feed["content"]
                )
                _, isCreated = models.Feed.get_or_create(
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
                cnt += isCreated
            time.sleep(1)
            if cnt != 20:
                logger.info("Page End")
                break
        time.sleep(5)
except KeyboardInterrupt:
    logger.critical('user aborted.')