from Crypto.PublicKey import RSA

def rsa_keys_client() -> tuple[bytes, bytes]:
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key , public_key

CLIENT_PRIVATE_KEY, CLIENT_PUBLIC_KEY = rsa_keys_client()

def get_rsa_public_key_client() -> bytes:
    """Get clients rsa public key"""
    return CLIENT_PUBLIC_KEY

