import secrets
import random 
import base64
from rsa_key_generation_client import rsa_keys_client

def session_generator():
    session_id = secrets.token_hex(16)
    return session_id


def random_number() -> int:
    random_int = random.randint(1,24)
    return random_int

def secure_connection_packet() -> str:
    """" converts the rsa_public_key from bytes to base64 and the from base64 to string"""
    rsa_public_key = rsa_keys_client()[1]
    encoded_public_key = base64.b64encode(rsa_public_key)
    return f'(CC,{encoded_public_key.decode("utf-8")})'