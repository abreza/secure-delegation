import json
from connection.tcp_socket import send_message
from utils import check_password, make_password
from peewee import *
from datetime import datetime

from os.path import exists

import configparser
config = configparser.ConfigParser()
config.read('../../app.cfg')

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
    policy_receiver = CharField(null=True)

    def check_policy(self, amount, receiver):
        if amount > self.policy_range:
            raise Exception('deligation policy range issue!')

        if datetime.now() > self.policy_timeout:
            raise Exception('deligation expired!')

    def sellCoin(self, amount):
        ip = config['EC']['IP']
        port = int(config['EC']['Port'])
        message = json.dump(
            {"url": "sell", "public_key": self.public_key, "amount": amount})
        response = send_message(ip, port, message)
        if response != 'OK':
            raise Exception('blockchain error ' + response)


class User(BaseModel):
    username = CharField(unique=True, max_length=128)
    password = CharField(max_length=128, default='pass')
    balance = IntegerField(default=1000000)
    blockchainDeligation = ForeignKeyField(
        BlockchainDeligation, null=True, unique=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def sellCoin(self, amount):
        self.blockchainDeligation.sellCoin(amount)
        self.balance += amount
        self.save()

    def exchangeCoin(self, receiver, amount):
        if not self.blockchainDeligation:
            raise Exception('deligation was not set!')

        self.blockchainDeligation.check_policy(amount, receiver)
        self.sellCoin(amount)

        transaction = Transaction.create(
            sender=self, receiver=receiver, amount=amount)
        transaction.save()

    def deligate(self, public_key, private_key, policy_range, policy_count, policy_timeout):
        self.blockchainDeligation = BlockchainDeligation.create(public_key, private_key,
                                                                policy_range, policy_count, policy_timeout)
        self.blockchainDeligation.save()
        self.save()

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
