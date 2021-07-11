import os
import hashlib


def make_password(raw_password):
    salt = os.urandom(32)
    hsh = hashlib.pbkdf2_hmac(
        'sha256', raw_password.encode('utf-8'), salt, 100000)
    return '%s$%s' % (salt, hsh)


def check_password(raw_password, enc_password):
    salt, hsh = enc_password.split('$', 1)
    return hsh == hashlib.pbkdf2_hmac('sha256', raw_password.encode('utf-8'), salt, 100000)
