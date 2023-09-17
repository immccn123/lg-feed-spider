"""
数据库配置，敏感文件。
**不要提交给版本控制系统！**
**不要修改！**
"""

import sys
from peewee import PostgresqlDatabase, OperationalError
from tools.logger import HandleLog

logger = HandleLog()
logger.info("connecting database......")


def get_connection():
    """获取一个数据库连接。"""
    try:
        main_database = PostgresqlDatabase(
            'lgfeed',
            thread_safe=True,
            autorollback=False,
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
