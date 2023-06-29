from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase

# db = SqliteDatabase('feed.db')

# db = MySQLDatabase(
#     "u933163999_lgfeed",
#     host="82.180.152.175",
#     user="u933163999_imken2",
#     password="imkenhaomeng!_QwQ0",
#     charset="utf8mb4",
#     port=3306,
# )

# db = MySQLDatabase(
#     "luogu_feed",
#     host="sh-cynosdbmysql-grp-5hkhuwxc.sql.tencentcdb.com",
#     user="luogu_feed",
#     password="Nrnq8fHZx7kWZc",
#     charset="utf8mb4",
#     port=28315,
# )


db = PostgresqlDatabase(
    'lgfeed',
    thread_safe=True,
    # thread_safe=False,
    autorollback=False,
    # user='immccn123',
    # host='localhost',
)
