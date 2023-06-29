'''
查询用程序，接受可选参数uid和username
'''

from db import models

query_uid = input('[leave blank if no] user uid      = ').strip()
query_username = input('[leave blank if no] user username = ').strip()

res = models.Feed.select()

if query_uid != '':
    res = res.where(models.Feed.user_id == int(query_uid))

if query_username != '':
    res = res.where(models.Feed.username == query_username)

for feed in res:
    print(feed.time,f'{feed.username}#{feed.user_id} : {feed.content}')
