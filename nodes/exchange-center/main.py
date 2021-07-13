import sys
import os

sys.path.append(os.path.abspath(os.path.join('../..', 'connection')))
from tcp_socket import listen
from request_handler import request_handler


def price():
    pass


def exchange():
    pass


router = {
    'price': price,
    'exchange': exchange
}

import configparser
config = configparser.ConfigParser()
config.read('../../app.cfg')
listen(lambda req: request_handler(req, router),
       host=config['EC']['IP'], port=int(config['EC']['Port']))
