from client_prompting import encryption_type , encryption_choice
from session import session_generator , random_number
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def start_packet() -> list[str]:
    secure_flag = encryption_type()
    packet = ["SS" , "RFMP" , "v1.0" , str(secure_flag)]
    return packet

def algo_and_encrypted_session(server_public_key: bytes) -> tuple[str , str]:
    """ algorithm and encryption type

        - Aes: random int -> 
        - Caesar : rsa encryption(binary bytes) -> base64 bytes -> decode utf-8 (converts base64 bytes into string)
    
    """
    algorithm = encryption_choice()
    rsa_key = RSA.import_key(server_public_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)

    if algorithm == "aes":
        session_id = session_generator()          
        session_key = bytes.fromhex(session_id)       
        encrypted_aes_with_server_public_key = cipher_rsa.encrypt(session_key)
        base64_conversion = base64.b64encode(encrypted_aes_with_server_public_key).decode("utf-8")
        return algorithm , base64_conversion

    elif algorithm == "caesar":
        shift = random_number()                   
        caeser = shift.to_bytes(1, "big")     
        encrypted_caeser_with_server_public_key = cipher_rsa.encrypt(caeser)
        base64_conversion = base64.b64encode(encrypted_caeser_with_server_public_key).decode("utf-8")
        return algorithm, base64_conversion


def packet_formatter(packet) -> str:
    """ this packet formatter function formats the initial packet"""
    message = "(" + ",".join(packet) + ")"
    return message