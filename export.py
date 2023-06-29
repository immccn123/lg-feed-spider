import datetime, json
from db import db, models

feeds = []

for feed in models.Feed.select():
    feeds.append(
        {
            "user": str(feed.username) + "#" + str(feed.user_id),
            "time": feed.time.timestamp(),
            "color": feed.user_color,
            "content": feed.content,
            "grub_time": feed.grub_time.timestamp(),
        }
    )

f = open(
    "export_%d.json" % (int(datetime.datetime.now().timestamp())), "w", encoding="utf-8"
)
s = json.dumps(feeds)

f.write(s)
f.close()
