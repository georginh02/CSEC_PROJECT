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

