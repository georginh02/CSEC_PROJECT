import base64

def rsa_public_key_converter( connection_packet: str) -> bytes:
    encoded_public_key = connection_packet.split(",")
    server_public_key = "".join(encoded_public_key[-1]).strip(")")
    decoded_server_public_key = base64.b64decode(server_public_key)
    return decoded_server_public_key
