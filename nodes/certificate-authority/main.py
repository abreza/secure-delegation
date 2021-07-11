import sys
import os

sys.path.append(os.path.abspath(os.path.join('../..', 'connection')))
from tcp_socket import listen


def request_handler(request):
    return 'response'


listen(request_handler)
