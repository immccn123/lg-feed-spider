"""
将数据库格式导出为 json 格式。
"""

import datetime
import json
from db import models
from tools.logger import HandleLog

logger = HandleLog()

feeds = []

def mainloop():
    '''主要逻辑，见上'''
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

    logger.info(f"Writing file {filename}...")

    write_stream = open(filename, "w", encoding="utf-8")
    write_content = json.dumps(feeds)

    write_stream.write(write_content)
    write_stream.close()

    logger.info(f"File saved as '{filename}'")
