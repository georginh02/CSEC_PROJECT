from rsa_key_generation_server import rsa_keys_server
import base64

def not_secure_packet() -> str:
    return "(" +"CC"+ ")"

def secure_connection_packet() -> str:
    """" converts the rsa_public_key from bytes to base64 and the from base64 to string"""
    rsa_public_key = rsa_keys_server()[1]
    encoded_public_key = base64.b64encode(rsa_public_key)
    return f'(CC,{encoded_public_key.decode("utf-8")})'
