"""
数据库配置，敏感文件。
"""

import sys
from peewee import MySQLDatabase, OperationalError
from tools.logger import HandleLog

logger = HandleLog()
logger.info("connecting database......")


def get_connection():
    """获取一个数据库连接。"""
    try:
        # main_database = SqliteDatabase("feed.main_database")
        # main_database = MySQLDatabase(
        #     "u933163999_lgfeed",
        #     host="82.180.152.175",
        #     user="u933163999_imken2",
        #     password="imkenhaomeng!_QwQ0",
        #     charset="utf8mb4",
        #     port=3306,
        # )
        # main_database = PostgresqlDatabase(
        #     'lgfeed',
        #     thread_safe=True,
        #     # thread_safe=False,
        #     autorollback=False,
        #     # user='immccn123',
        #     # host='localhost',
        # )
        main_database = MySQLDatabase(
            "luogu_feed",
            host="sh-cynosmain_databasemysql-grp-5hkhuwxc.sql.tencentcmain_database.com",
            user="luogu_feed",
            password="Nrnq8fHZx7kWZc",
            charset="utf8mb4",
            port=28315,
        )
        main_database.connect()
    except OperationalError as exception_occurred:
        main_database.close()
        logger.critical("Cannot connect to database with these exceptions:")
        print(exception_occurred)
        logger.critical("Aborted.")
        sys.exit(1)
    logger.info("Connected to database.")
    return main_database
