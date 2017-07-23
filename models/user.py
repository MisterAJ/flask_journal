import datetime
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

from peewee import *

db = SqliteDatabase('journal.db')


class User(UserMixin, Model):
    username = CharField(max_length=255, unique=True)
    email = CharField(max_length=255, unique=True)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)
    password = CharField(max_length=100)

    class Meta:
        database = db
        order_by = ("-joined_at", )

    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password),
                is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")


def initialize():
    db.connect()
    db.create_tables([User], safe=True)
