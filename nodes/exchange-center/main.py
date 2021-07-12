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

listen(lambda req: request_handler(req, router))
