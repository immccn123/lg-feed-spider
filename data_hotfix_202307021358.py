from db.models import Feed
from datetime import timedelta
from peewee import *

# 获取时间差为8小时的时间范围
time_difference = timedelta(hours=8, seconds=2)

# 查询满足条件的Feed对象
query = (
    Feed.select()
    .join(Feed, on=(Feed.content == Feed.content) & (Feed.time != Feed.time))
    .where((Feed.time - Feed.time).between(-time_difference, time_difference))
)

# 遍历查询结果，删除时间较早的对象
for feed in query:
    # 获取时间较早的对象
    earliest_feed = (
        Feed.select()
        .where((Feed.content == feed.content) & (Feed.time != feed.time))
        .order_by(Feed.time)
        .first()
    )

    # 删除时间较早的对象
    earliest_feed.delete_instance()
