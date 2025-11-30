import base64

def rsa_public_key_converter( connection_packet: str) -> bytes:
    """---- decode from string to bytes"""
    encoded_public_key = connection_packet.split(",")
    server_public_key = "".join(encoded_public_key[-1]).strip(")")
    decoded_server_public_key = server_public_key.encode("utf-8")
    return decoded_server_public_key


def get_server_rsa_public_key(server_public_key: bytes) :
    """Get servers public key from the client to then use it in the packets file"""
    return server_public_key
    

