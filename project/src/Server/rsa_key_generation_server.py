from Crypto.PublicKey import RSA

def rsa_keys_server() -> tuple[bytes, bytes]:
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

SERVER_PRIVATE_KEY, SERVER_PUBLIC_KEY = rsa_keys_server()

def get_rsa_public_key_client() -> bytes:
    """Get server rsa public key"""
    return SERVER_PUBLIC_KEY
    

def get_rsa_private_key() -> bytes:
    """Get servers private key"""
    return SERVER_PRIVATE_KEY



