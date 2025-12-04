from rsa_key_generation_server import get_rsa_public_key_client
import base64

 #-----------------------------------------
 # Step 6 if not secure
def not_secure_packet() -> str:
    """ if the setup packet recived from the client returns false in the function is_secure then we will call this function"""
    return "(" +"CC"+ ")"

 #-----------------------------------------

 #-----------------------------------------
 # Step 6 if it is secure
 
def secure_connection_packet() -> str:
    """" converts the rsa_public_key from bytes to base64 and the from base64 to string and also if the setup packet recived from the client returns true in the function is_secure then we will call this function"""
    rsa_public_key = get_rsa_public_key_client()
    return f'(CC,{rsa_public_key.decode("utf-8")})'
 #-----------------------------------------
 