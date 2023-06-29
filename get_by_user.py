from db import db, models

uid = 627636

for feed in models.Feed.select().where(models.Feed.user_id == uid).order_by(models.Feed.time):
    print(feed.content.replace('\n', ' \\ '))
