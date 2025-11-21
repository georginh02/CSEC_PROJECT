from client_prompting import encryption_type

def start_packet() -> list[str]:
    secure_flag = encryption_type()
    packet = ["SS" , "RFMP" , "v1.0" , str(secure_flag)]
    return packet

def encryption_packet() -> str:
    return "(" + "EC" + ""

def packet_formatter(packet) -> str:
    message = "(" + ",".join(packet) + ")"
    return message