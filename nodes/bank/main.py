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


def deliagte(request):
    try:
        username = request['username']
        password = request['password']
        public_key = request['public_key']
        private_key = request['private_key']
        policy_range = request['policy_range']
        policy_count = request['policy_count']
        policy_timeout = request['policy_timeout']
    except:
        return 'Error: bad request!'

    try:
        user = User.authenticate(username, password)
    except User.DoesNotExist:
        return 'Error: invalid username or password!'

    user.deligate(public_key,
                  private_key,
                  policy_range,
                  policy_count,
                  policy_timeout)
    return 'OK'


def buyWithCoin(request):
    username = request.get('username')
    password = request.get('password')
    receiver = request.get('receiver')
    amount = request.get('amount')

    if not username or not password or not receiver or not amount:
        return 'Error: bad request! Req should have username, password, receiver and amount fields.'
    try:
        user = User.authenticate(username, password)
    except User.DoesNotExist:
        return 'Error: invalid username or password!'

    try:
        receiver = User.select().where(username == receiver)
    except User.DoesNotExist:
        return 'Error: receiver does not exist!'

    try:
        user.exchangeCoin(receiver, amount)
    except Exception as e:
        return 'Error: ' + e


router = {
    'checkBalance': checkBalance,
    'createAccount': createAccount,
    'deliagte': deliagte,
    'buyWithCoin': buyWithCoin,
}

import configparser
config = configparser.ConfigParser()
config.read('../../app.cfg')

listen(lambda req: request_handler(req, router),
       host=config['BANK']['IP'], port=int(config['BANK']['Port']))
