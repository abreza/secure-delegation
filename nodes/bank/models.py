from utils import check_password, make_password
from peewee import *

from os.path import exists

db_name = 'db.sqlite3'
database = SqliteDatabase(db_name)


class BaseModel(Model):
    class Meta:
        database = database


class BlockchainDeligation(BaseModel):
    public_key = CharField(unique=True)
    private_key = CharField(unique=True)
    policy_range = IntegerField()
    policy_count = IntegerField()
    policy_timeout = DateTimeField()
    policy_receiver = CharField()


class User(BaseModel):
    username = CharField(unique=True, max_length=128)
    password = CharField(max_length=128, default='pass')
    balance = IntegerField(default=1000000)
    blockchainAccount = ForeignKeyField(
        BlockchainDeligation, null=True, unique=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @staticmethod
    def authenticate(username, password):
        user = User.select().where(User.username == username).get()

        if not user.check_password(password):
            raise User.DoesNotExist

        return user


class Transaction(BaseModel):
    sender = ForeignKeyField(User)
    receiver = ForeignKeyField(User)
    amount = IntegerField()

    def save(self, *args, **kwargs):
        if self.sender.balance < self.amount:
            raise Exception('There is not enough balance!')

        self.sender.balance -= self.amount
        self.receiver.balance += self.amount
        return super(Transaction, self).save(*args, **kwargs)


def create_tables():
    with database:
        database.create_tables([User, Transaction, BlockchainDeligation])


if not exists(db_name):
    create_tables()
