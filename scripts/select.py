"""
查询用程序，接受可选参数 uid 和 username
"""

import re

from db import models


def mainloop():
    """主要逻辑，见上"""
    query_uid = input("[Leave blank if no] user uid       = ").strip()
    query_username = input("[Leave blank if no] user username  = ").strip()
    query_keyword = input("[Leave blank if no] msg  keyword   = ").strip()

    res = models.Feed.select()

    if query_uid != "":
        res = res.where(models.Feed.user_id == int(query_uid))

    if query_username != "":
        res = res.where(models.Feed.username == query_username)

    if query_keyword != "":
        res = res.where(models.Feed.content.like(f"%{query_keyword}%"))

    for feed in res:
        content = feed.content.replace("\n", " / ")
        content = re.sub(r"\[(\S+)\]\(/user/(\d+)\)", r"\g<1>#\g<2>", content)
        print(feed.time, f"{feed.username}#{feed.user_id} : {content}")
