import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join('../..', 'connection')))
from tcp_socket import listen


def request_handler(request):
    try:
        req = json.loads(request)
    except:
        return 'Error: bad request! Req should be stringified json.'
    url = req.get('url')
    if not url:
        return 'Error: bad request! Req should have a url field.'

    if req.get('url') == 'price':
        pass
    if req.get('url') == 'exchange':
        pass
    return 'Error: bad url!'


listen(request_handler)
