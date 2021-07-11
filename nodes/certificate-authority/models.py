from peewee import *

from generate_certificate import generate_x509

database = SqliteDatabase('db.sqlite3')


class BaseModel(Model):
    class Meta:
        database = database


class Certificate(BaseModel):
    address = CharField(unique=True)
    public_key = CharField(unique=True)

    def generate_certificate(self):
        return generate_x509(self.address, self.public_key)
