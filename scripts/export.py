'''
将数据库格式导出为json格式。
'''

import datetime
import json
from db import models
from tools.logger import HandleLog

logger = HandleLog()

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

filename = f"export_{int(datetime.datetime.now().timestamp())}.json"

logger.info(f'writing in file {filename}')
f = open(
    filename , "w", encoding="utf-8"
)
s = json.dumps(feeds)

f.write(s)
f.close()

logger.info(f'file saved as \'{filename}\'')
