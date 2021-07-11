from models import Certificate

address = "google.com"
public_key = """-----BEGIN PUBLIC KEY-----
MIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgG/HXNd+s7IUk7sR4GJlis7qgxjy
/syeFv32qu9Bqg6Gmo68m9lkJmsxTu1Rj9X8zGMD7Ibs0u36j8fPil063Vj/+Wvf
QJWFsErxswMcXXg3RZ9ojnWHFYmcefJZ+eoLPwAIHi9B1uO4nwk6n2EX/HwKjR2V
g15GFTTfMg5ZlL9xAgMBAAE=
-----END PUBLIC KEY-----"""

cert = Certificate.create(address=address, public_key=public_key)
cert.save()

print(cert.generate_certificate())
