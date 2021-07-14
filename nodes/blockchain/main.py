import sys
import os

sys.path.append(os.path.abspath(os.path.join('../..', 'connection')))
from tcp_socket import listen
from request_handler import request_handler


def addNewBlock(request):
    pass


def concession(request):
    public_key = request['public_key']
    policy_range = request['policy_range']
    policy_count = request['policy_count']
    policy_timeout = request['policy_timeout']
    pass


def exchange(request):
    request.get('seller')
    request.get('buyer')
    request.get('amount')
    request.get('isDeligated')
    pass


router = {
    'addNewBlock': addNewBlock,
    'concession': concession,
    'exchange': exchange
}

import configparser
config = configparser.ConfigParser()
config.read('../../app.cfg')
listen(lambda req: request_handler(req, router),
       host=config['BLACKCHAIN']['IP'], port=int(config['BLACKCHAIN']['Port']))
