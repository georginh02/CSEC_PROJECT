from session import session_generator , random_number
from rsa_key_generation_client import get_rsa_public_key_client
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP , AES  
from Crypto.Hash import SHA256
import base64

ALGO = None      
AES_SESSION_KEY = None    
CAESAR_SHIFT = None  

#----------------------------------------------------------------
# step 1
def encryption_type() -> int:
    """
    asks the client if they want encrypted communication or not
     
    Encrypted:
    - If the client selects number 1 then the function will store number one 

    Non Encrypted:
    - if the client selects number 0 then the function will store number one 
    
    """
    start_packet_options= {
        "Non Secured RFMP v1.0": 0 ,
        "Secured RFMP v1.0" : 1
        }
    message = f"If you want to use {list(start_packet_options.keys())[0]} please enter 0 or please enter 1 for {list(start_packet_options.keys())[1]}: "
    
    # the try and except block here is to prevent the user from picking characters 
    try:
        user_inp = int(input(message))
    except ValueError as e:
        print("Please enter either 0 or 1")
        return encryption_type()
    
    # 
    if user_inp not in start_packet_options.values() :
        print("Please enter either 0 or 1")
        return encryption_type()
    elif user_inp == 0:
        print(f"you have selected {list(start_packet_options.keys())[0]}")
        return start_packet_options["Non Secured RFMP v1.0"]
    else:
        print(f"you have selected {list(start_packet_options.keys())[1]}")
        return start_packet_options["Secured RFMP v1.0"]

def start_packet() -> list[str]:
    """ this start packet function waits for the user to choose if he wants encryption or not and then formats it in packet = ["SS" , "RFMP" , "v1.0" , ("0" or "1") -> this is the users choice from encryption_packet]   """
    secure_flag = encryption_type()
    packet = ["SS" , "RFMP" , "v1.0" , str(secure_flag)]
    return packet

def packet_formatter(packet) -> str:
    """ this packet formatter function formats the initial packet // so what it does is adds () to the start and the end and joins the list with , at the end of each index"""
    message = "(" + ",".join(packet) + ")"
    return message
#------------------------------------------

# Step 10

def encryption_choice() -> str:
    """client chooses either aes or ceaser encryption"""
    user_input = input("what type of encryption do you want Aes or Caesar: ")
    if user_input.lower()== "aes":
        return user_input.lower()
    elif user_input.lower() == "caesar":
        return user_input.lower()
    else:
         print("pls enter a proper option")
         return encryption_choice() 
         

def algo_and_encrypted_session(server_public_key: bytes) -> tuple[str , str]:
    """
        user selects the encryption tye he wants either aes or ceaser then we encrypt the session key

    """
    global ALGO , AES_SESSION_KEY , CAESAR_SHIFT
    
    algorithm = encryption_choice() 
    rsa_key = RSA.import_key(server_public_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key , SHA256)

    if algorithm == "aes":
        session_id = session_generator()          
        session_key = bytes.fromhex(session_id)       
        encrypted_aes_with_server_public_key = cipher_rsa.encrypt(session_key)
        base64_conversion = base64.b64encode(encrypted_aes_with_server_public_key).decode("utf-8")
        
        ALGO = "aes"
        AES_SESSION_KEY = session_key
        CAESAR_SHIFT = None
        
        return algorithm , base64_conversion
    
    elif algorithm == "caesar":
        shift = random_number()                   
        caeser = shift.to_bytes(1, "big")     
        encrypted_caeser_with_server_public_key = cipher_rsa.encrypt(caeser)
        base64_conversion = base64.b64encode(encrypted_caeser_with_server_public_key).decode("utf-8")
        
        ALGO = "caesar"
        CAESAR_SHIFT = shift
        AES_SESSION_KEY = None
        
        return algorithm, base64_conversion

def ec_packet(server_public_key: bytes) -> str:
    """ here we the complete ec packet , we call this function in the client_side"""
    algorithm , base64_conversion = algo_and_encrypted_session(server_public_key)
    client_rsa_public_key = get_rsa_public_key_client()
    client_rsa_public_key = client_rsa_public_key.decode("utf-8")
    complete_ec_packet = "(" +"EC" + "," + algorithm + ","  + base64_conversion + "," + client_rsa_public_key + ")"
    return complete_ec_packet

#------------------------------------------
def encrypt_data_if_secure(plaintext: str) -> str:
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


def decrypt_data_if_secure(ciphertext: str) -> str:
    """
    same logic as before but it decrypts text depending on the algorithm chosen
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