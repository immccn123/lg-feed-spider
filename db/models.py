"""
用于定义数据库模型，非必要不要动。
"""

from peewee import CharField, DateTimeField, IntegerField, Model

from tools.logger import HandleLog
from .config import get_connection

logger = HandleLog()


class Feed(Model):
    """
    犇犇对象，包含信息如下
    """

    user_id = IntegerField()
    user_color = CharField()
    username = CharField()

    time = DateTimeField()
    content = CharField(max_length=8192)
    hash = CharField(unique=True, max_length=512)

    grub_time = DateTimeField()

    class Meta:
        """
        元信息。给 ORM 看的。
        """

        database = get_connection()


if not Feed.table_exists():
    logger.warning("Table 'feed' not found, creating...")
    Feed.create_table(False)
    logger.info("Table 'feed' created.")
