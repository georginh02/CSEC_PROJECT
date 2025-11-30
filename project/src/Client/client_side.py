import socket
from client_prompting import user_commands 
from packets import start_packet , packet_formatter ,  ec_packet
from helpers import rsa_public_key_converter 


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.gethostname()
    port = 8080

    s.connect((host, port))

    # Sending intitial setup packet to server
    initial_message = packet_formatter(start_packet())
    print(f"sending {initial_message} packet to server...")
    s.send(initial_message.encode("utf-8"))

    # Awaiting response from the server for unencrypted communication or encrypted communication
    data_recived = s.recv(1024)
    decoded_response_from_server = data_recived.decode("utf-8")
    
    if len(decoded_response_from_server.strip("()")) == 2:
        
        #If we only recive the CC packet from the server we will contiune with the unencrypted communication
        print(f"reciving response from server: {decoded_response_from_server}")

    if len(decoded_response_from_server.strip("()")) > 2:
        
        # Now if the communication is encrypted then we have to first recive the Confirm-Connection-Packet and then send out the Encryption-Packet       
        print(f"reciving connection packet from server: {decoded_response_from_server}")
        
        # use the rsa_public_key_converter to remove all unessecary data and just get the proper formatted servers public key
        decoded_servers_public_key = rsa_public_key_converter(decoded_response_from_server)
        
        # send the decoded_servers_public_key into the ec_packet function so it can make the paket to send back to the server
        complete_ec_packet = ec_packet(decoded_servers_public_key)
        s.send(complete_ec_packet.encode("utf-8"))
        print(f"sending ec packet to server {complete_ec_packet}")
        
    while True:
        user_choice = user_commands()  
        s.send(user_choice.encode("utf-8"))
        print(f"sending users choice and complete cm packet to server: {user_choice}")
        
main()