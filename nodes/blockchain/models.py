from peewee import *

from os.path import exists

db_name = 'db.sqlite3'
database = SqliteDatabase(db_name)


class BaseModel(Model):
    class Meta:
        database = database


class Block(BaseModel):
    pass


def create_tables():
    with database:
        database.create_tables([Block])


if not exists(db_name):
    create_tables()
