from Crypto.PublicKey import RSA

def rsa_keys_server() -> tuple[bytes, bytes]:
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key , public_key
