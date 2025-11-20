from project.src.Client.client_prompting import encryption_type

def start_packet() -> list:
    secure_flag = encryption_type()
    packet = ["SS" , "RMFP" , "v1.0" , secure_flag]
    return packet

def main():
    print(start_packet())

if __name__ == "__main__":
    main()
