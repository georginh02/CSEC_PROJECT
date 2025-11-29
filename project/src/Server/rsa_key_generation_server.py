from Crypto.PublicKey import RSA

def rsa_keys_server() -> tuple[bytes, bytes]:
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key , public_key


def get_rsa_public_key_client() -> bytes:
    """Get server rsa public key"""
    private , public = rsa_keys_server()
    return public
