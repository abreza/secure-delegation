import sys
import os

sys.path.append(os.path.abspath(os.path.join('../..', 'connection')))
from tcp_socket import listen
from request_handler import request_handler


def addNewBlock():
    pass


def concession():
    pass


router = {
    'addNewBlock': addNewBlock,
    'concession': concession
}

import configparser
config = configparser.ConfigParser()
config.read('../../app.cfg')
listen(lambda req: request_handler(req, router),
       host=config['BLACKCHAIN']['IP'], port=int(config['BLACKCHAIN']['Port']))
