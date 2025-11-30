from rsa_key_generation_server import get_rsa_private_key
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
import base64

def decrypt_ec_packet(ec_packet: str) -> tuple[str, bytes , str]:
    severs_private_key = get_rsa_private_key()
    stripping_brackets = ec_packet.strip("()").split(",")
    private_key = RSA.import_key(severs_private_key)
    cipher_rsa = PKCS1_OAEP.new(private_key , SHA256)
    algorithm = stripping_brackets[1]
    
    if algorithm in ("aes", "caesar"):
        session_id = stripping_brackets[2].strip()
        client_public_key = stripping_brackets[3]
        encrypted_session_bytes = base64.b64decode(session_id)
        session_key = cipher_rsa.decrypt(encrypted_session_bytes)
        # ses = session_key.hex().strip()
        return algorithm , session_key , client_public_key
