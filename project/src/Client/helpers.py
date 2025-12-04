
# ---------------------------------------------
# step 9

def rsa_public_key_converter( connection_packet: str) -> bytes:
    """decode the rsa key from bytes to string"""
    encoded_public_key = connection_packet.split(",")
    server_public_key = "".join(encoded_public_key[-1]).strip(")")
    decoded_server_public_key = server_public_key.encode("utf-8")
    return decoded_server_public_key


