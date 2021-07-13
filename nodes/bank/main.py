from models import User
import sys
import os
from peewee import IntegrityError


sys.path.append(os.path.abspath(os.path.join('../..', 'connection')))
from tcp_socket import listen
from request_handler import request_handler


def checkBalance(request):
    username = request.get('username')
    password = request.get('password')
    if not username or not password:
        return 'Error: bad request! Req should have username and password fields.'
    try:
        user = User.authenticate(username, password)
        return str(user.balance)
    except User.DoesNotExist:
        return 'Error: invalid username or password!'


def createAccount(request):
    username = request.get('username')
    password = request.get('password')
    if not username or not password:
        return 'Error: bad request! Req should have username and password fields.'

    try:
        user = User.create(username=username)
        user.set_password(password)
        user.save()
        return 'Account created!'
    except IntegrityError as e:
        print(e)
        return 'Error: user already exist!'


router = {
    'checkBalance': checkBalance,
    'createAccount': createAccount
}

import configparser
config = configparser.ConfigParser()
config.read('../../app.cfg')

listen(lambda req: request_handler(req, router),
       host=config['BANK']['IP'], port=int(config['BANK']['Port']))
