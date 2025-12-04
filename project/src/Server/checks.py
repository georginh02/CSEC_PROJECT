
 #-----------------------------------------
 # Step 4 
 
def is_secure(setup_packet:str) -> bool:
    """ the function is secure checks if the string after stripping () ends with 1 which it then returs true , else it returns false that means no encryption is needed"""
    m1 = setup_packet.strip("()")
    if m1.endswith("1"):
        return True
    return False

 #-----------------------------------------