import secrets
import random 

def session_generator():
    """ generate random session_id"""
    session_id = secrets.token_hex(16)
    return session_id


def random_number() -> int:
    """Generate a random integer from 1 to 24"""
    random_int = random.randint(1,24)
    return random_int

