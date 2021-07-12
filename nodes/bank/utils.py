import random
import string
import hashlib


def make_password(raw_password):
    salt = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=32))
    hsh = hashlib.pbkdf2_hmac(
        'sha256', raw_password.encode(), salt.encode(), 100000)
    return '%s$%s' % (salt, hsh)


def check_password(raw_password, enc_password):
    salt, hsh = enc_password.split('$', 1)
    pass_hsh = str(hashlib.pbkdf2_hmac(
        'sha256', raw_password.encode(), salt.encode(), 100000))
    return hsh == pass_hsh
