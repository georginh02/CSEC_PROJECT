
def is_secure(setup_packet:str) -> bool:
    m1 = setup_packet.strip("()")
    if m1.endswith("1"):
        return True
    return False