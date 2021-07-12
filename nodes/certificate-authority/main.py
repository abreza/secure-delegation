from x509_certificate import verify
from models import Certificate
import sys
import os

sys.path.append(os.path.abspath(os.path.join('../..', 'connection')))
from tcp_socket import listen
from request_handler import request_handler


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


router = {
    # example {"url": "verify", "address": "google.com", "public_key": "salam", "certificate": "1234"}
    'verify': verify,
    'certificates': get_certificates
}

listen(lambda req: request_handler(req, router), '127.0.0.1', 8081)
