from rsa_key_generation_server import get_rsa_private_key
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP , AES
from Crypto.Hash import SHA256
import base64

ALGO = None
AES_SESSION_KEY = None
CAESAR_SHIFT = None

#--------------------------------------------------------
# Step 13
def decrypt_ec_packet(ec_packet: str) -> tuple[str, bytes , str]:
    global ALGO, AES_SESSION_KEY, CAESAR_SHIFT
     
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
        #ses = session_key.hex().strip() -> if docter wants to see it decrypted pls uncomment
        
        if algorithm == "aes":
            ALGO = "aes"
            AES_SESSION_KEY = session_key       
            CAESAR_SHIFT = None

        elif algorithm == "caesar":
            ALGO = "caesar"
            CAESAR_SHIFT = session_key[0]      
            AES_SESSION_KEY = None

        return algorithm , session_key , client_public_key
    
#--------------------------------------------------------
def encrypt_data_if_secure_server(plaintext: str) -> str:
    """
    Encrypt text using the negotiated algorithm Aes or caesar if ALGO is set.
    If ALGO is None -> return plaintext as-is unencrypted comms.
    """
    if ALGO is None:
        return plaintext

    if ALGO == "aes":
        cipher = AES.new(AES_SESSION_KEY, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode("utf-8"))
        blob = nonce + tag + ciphertext
        return base64.b64encode(blob).decode("utf-8")

    if ALGO == "caesar":
        shift = CAESAR_SHIFT
        return "".join(chr((ord(c) + shift) % 256) for c in plaintext)

    return plaintext


def decrypt_data_if_secure_server(ciphertext: str) -> str:
    """
    same logic as before.
    same logic as before.
    """
    if ALGO is None:
        return ciphertext

    if ALGO == "aes":
        raw = base64.b64decode(ciphertext.encode("utf-8"))
        nonce = raw[:16]
        tag = raw[16:32]
        ct = raw[32:]
        cipher = AES.new(AES_SESSION_KEY, AES.MODE_EAX, nonce=nonce)
        pt = cipher.decrypt_and_verify(ct, tag)
        return pt.decode("utf-8")

    if ALGO == "caesar":
        shift = CAESAR_SHIFT
        return "".join(chr((ord(c) - shift) % 256) for c in ciphertext)

    return ciphertext