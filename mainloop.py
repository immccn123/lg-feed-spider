import datetime
import json
import time

import requests

from db import db, models
from utils import calc_feed_hash

print("[Init] Connecting to Database... ", end="")

if not db.is_connection_usable():
    db.connect()

print("Done.")

while True:
    k = 1
    while True:
        print("page", k)
        k += 1
        is_created = 0
        r = requests.get(
            "https://www.luogu.com.cn/api/feed/list?page=" + str(k),
            headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
            },
        ).text
        r: list = json.loads(r)["feeds"]["result"]
        if len(r) == 0:
            break
        for feed in r:
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
        time.sleep(1)
        if not is_created:
            print("Page End")
            break
    time.sleep(5)
