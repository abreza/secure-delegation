import sys
import os

sys.path.append(os.path.abspath(os.path.join('../..', 'connection')))
from tcp_socket import listen
from request_handler import request_handler


def checkBalance():
    pass


router = {
    'checkBalance': checkBalance
}

listen(lambda req: request_handler(req, router))
