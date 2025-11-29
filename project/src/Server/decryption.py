from rsa_key_generation_server import get_rsa_private_key

def decrypt_ec_packet(ec_packet: str):
    severs_private_key = get_rsa_private_key()
    print("here" + ec_packet)

