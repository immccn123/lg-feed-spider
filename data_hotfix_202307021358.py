from db import models
from datetime import timedelta
from peewee import *

# 获取时间差为8小时的时间范围
time_difference = timedelta(hours=8, seconds=2)

# 查询满足条件的models.Feed对象
query = (
    models.Feed.select()
    .join(models.Feed, on=(models.Feed.content == models.Feed.content) & (models.Feed.time != models.Feed.time))
    .where((models.Feed.time - models.Feed.time).between(-time_difference, time_difference))
)

# 遍历查询结果，删除时间较早的对象
for models.Feed in query:
    # 获取时间较早的对象
    earliest_feed = (
        models.Feed.select()
        .where((models.Feed.content == models.Feed.content) & (models.Feed.time != models.Feed.time))
        .order_by(models.Feed.time)
        .first()
    )

    # 删除时间较早的对象
    earliest_feed.delete_instance()
