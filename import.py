import json
import datetime

from utils import calc_feed_hash
from db import db, models

if not db.is_connection_usable():
    db.connect()

origin_file = json.load(open("export.json", "r", encoding="utf-8"))

cnt = 0

for feed in origin_file:
    cnt += 1
    print(cnt, "/", len(origin_file), end="\r")
    stime = feed["time"]
    user = feed["user"].split("#")[0]
    uid = int(feed["user"].split("#")[1])
    content = feed["content"]
    feed_hash = calc_feed_hash(uid, stime, content)
    _, is_created = models.Feed.get_or_create(
        hash=feed_hash,
        defaults={
            "user_id": uid,
            "user_color": feed["color"],
            "username": user,
            "time": datetime.datetime.fromtimestamp(stime),
            "content": content,
            "grub_time": datetime.datetime.now(),
        },
    )
