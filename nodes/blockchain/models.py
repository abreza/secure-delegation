from peewee import *

from os.path import exists

db_name = 'db.sqlite3'
database = SqliteDatabase(db_name)


class BaseModel(Model):
    class Meta:
        database = database


class Account():
    public_key = CharField(unique=True)


class Block(BaseModel):
    private_key = CharField(unique=True)
    public_key = CharField(unique=True)


class Transactions(BaseModel):
    block = ForeignKeyField(Block)
    sender = ForeignKeyField(Account)
    receiver = ForeignKeyField(Account)


class Deligation(BaseModel):
    block = ForeignKeyField(Block)
    public_key = CharField(unique=True)
    policy_range = IntegerField()
    policy_count = IntegerField()
    policy_timeout = DateTimeField()
    policy_receiver = CharField()


def create_tables():
    with database:
        database.create_tables([Account, Block, Transactions, Deligation])


if not exists(db_name):
    create_tables()
