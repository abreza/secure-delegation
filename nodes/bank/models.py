from utils import check_password, make_password
from peewee import *

from os.path import exists

db_name = 'db.sqlite3'
database = SqliteDatabase(db_name)


class BaseModel(Model):
    class Meta:
        database = database


class BlockchainAccount(BaseModel):
    public_key = CharField(unique=True)
    private_key = CharField(unique=True)


class User(BaseModel):
    username = CharField(unique=True, max_length=128)
    password = CharField(max_length=128)
    blockchainAccount = ForeignKeyField(
        BlockchainAccount, null=True, unique=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def authenticate(self, username, password):
        try:
            user = User.select().where(User.username == username).get()
        except User.DoesNotExist:
            return False

        if not user.check_password(password):
            return False

        return user


class Transaction(BaseModel):
    user = ForeignKeyField(User, backref='transactions')
    amount = IntegerField()


def create_tables():
    with database:
        database.create_tables([User, Transaction])


if not exists(db_name):
    create_tables()
