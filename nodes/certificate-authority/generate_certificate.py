from generate_key import generate_and_save_key
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import serialization

from os.path import exists


import datetime
one_day = datetime.timedelta(1, 0, 0)


def load_key():
    if not exists('private.key'):
        private_key = generate_and_save_key()
    else:
        with open("private.key", "r") as private_key_file:
            private_key = private_key_file.read()
    private_key = load_pem_private_key(
        private_key.encode(), None, default_backend())

    return private_key


private_key = load_key()


def generate_x509(address, pub_key):
    builder = x509.CertificateBuilder().subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, address),
    ])
    ).issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, address),
    ])
    ).not_valid_before(
        datetime.datetime.today() - one_day
    ).not_valid_after(
        datetime.datetime.today() + (one_day * 30)).serial_number(
            x509.random_serial_number()
    ).public_key(pub_key).add_extension(
        x509.SubjectAlternativeName(
            [x509.DNSName(address)]
        ),
        critical=False
    ).add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True,
    )

    certificate = builder.sign(
        private_key=private_key, algorithm=hashes.SHA256(),
    )

    return certificate.public_bytes(serialization.Encoding.PEM)
