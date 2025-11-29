from rsa_key_generation_server import get_rsa_public_key_client
import base64

def not_secure_packet() -> str:
    return "(" +"CC"+ ")"

def secure_connection_packet() -> str:
    """" converts the rsa_public_key from bytes to base64 and the from base64 to string"""
    rsa_public_key = get_rsa_public_key_client()
    return f'(CC,{rsa_public_key.decode("utf-8")})'
