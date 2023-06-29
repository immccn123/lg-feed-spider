from db import db, models

# keyword = '贴贴'
keyword = '原神'

for feed in models.Feed.select().where(models.Feed.content.contains(keyword)):
    print(feed.content)
