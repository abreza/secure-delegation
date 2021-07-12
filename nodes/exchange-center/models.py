from peewee import *

from os.path import exists

db_name = 'db.sqlite3'
database = SqliteDatabase(db_name)


class BaseModel(Model):
    class Meta:
        database = database


class Price(BaseModel):
    type = CharField(unique=True)
    amount = IntegerField()


def create_tables():
    with database:
        database.create_tables([Price])


if not exists(db_name):
    create_tables()
