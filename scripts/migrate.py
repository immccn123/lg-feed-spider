"""
导入最新版格式的数据。
"""

import json
import datetime
import sys

from db import  get_connection, models
from scripts.utils import calc_feed_hash
from tools.logger import HandleLog
from .utils import print_process

logger = HandleLog()

main_database = get_connection()

def main_loop():
    '''主要逻辑，见上'''
    with open(input("                    filename (json format):"),
               "r", encoding="utf-8") as read_stream:
        origin_file = json.load(read_stream.read())

    start_point = input('[leave blank if no]start from x-th message:')

    if start_point != '':
        try:
            cnt = int(start_point)-1
        except TypeError:
            logger.critical(f'cannot convert \'{start_point}\' into integer.')
            sys.exit(0)
    else:
        cnt = 0

    for feed in origin_file:
        cnt += 1
        print_process(cnt,len(origin_file))
        stime = feed["time"]
        user = feed["user"].split("#")[0]
        uid = int(feed["user"].split("#")[1])
        content = feed["content"]
        feed_hash = calc_feed_hash(uid, stime, content)
        models.Feed.get_or_create(
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
