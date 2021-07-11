from peewee import *

from generate_certificate import generate_x509

from os.path import exists

db_name = 'db.sqlite3'
database = SqliteDatabase(db_name)


class BaseModel(Model):
    class Meta:
        database = database


class Certificate(BaseModel):
    address = CharField(unique=True)
    public_key = CharField(unique=True)

    def generate_certificate(self):
        return generate_x509(self.address, self.public_key)


def create_tables():
    with database:
        database.create_tables([Certificate])


if not exists(db_name):
    create_tables()
