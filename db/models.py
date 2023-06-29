from peewee import CharField, DateTimeField, IntegerField, Model

from .config import db


class Feed(Model):
    user_id = IntegerField()
    user_color = CharField()
    username = CharField()

    time = DateTimeField()
    content = CharField(max_length=8192)
    hash = CharField(unique=True, max_length=512)

    grub_time = DateTimeField()

    class Meta:
        database = db

if not Feed.table_exists():
    Feed.create_table(False)
