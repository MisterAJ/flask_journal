import datetime

from flask.ext.login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('journal.db')


class Entry(UserMixin, Model):
    name = CharField(max_length=255, unique=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    text = TextField(default='')

    class Meta:
        database = DATABASE
        order_by = ("-created_at", )
