from x509_certificate import verify
from models import Certificate
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join('../..', 'connection')))
from tcp_socket import listen


def verify_certificate(req):
    address = req.get('address')
    public_key = req.get('public_key')
    certificate = req.get('certificate')
    if not address or not public_key or not certificate:
        return 'Error: bad request!'

    try:
        print(address, public_key, certificate)
        Certificate.select().where(Certificate.address == address,
                                   Certificate.public_key == public_key).get()

        if verify(public_key, certificate):
            return 'OK'
        return 'Error: invalid certificate!'
    except Certificate.DoesNotExist:
        return 'Error: certificate not found!'


def get_certificates():
    res = ''
    for certificate in Certificate.select():
        print(certificate)
        res += str(certificate)
    return res


def request_handler(request):
    try:
        req = json.loads(request)
    except:
        return 'Error: bad request! Req should be stringified json.'
    url = req.get('url')
    if not url:
        return 'Error: bad request! Req should have a url field.'
    # example {"url": "verify", "address": "google.com", "public_key": "salam", "certificate": "1234"}
    if req.get('url') == 'verify':
        return verify_certificate(req)

    if req.get('url') == 'certificates':
        return get_certificates()
    return 'Error: bad url!'


listen(request_handler, '127.0.0.1', 8081)
