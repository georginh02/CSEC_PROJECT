import socket
from packets import start_packet
from packets import packet_formatter
from helpers import rsa_public_key_converter
import base64

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.gethostname()
    port = 8083

    s.connect((host, port))

    """Sending intitial setup packet to server"""
    initial_message = packet_formatter(start_packet())
    print(f"sending {initial_message} packet to server...")
    s.send(initial_message.encode("utf-8"))

    """Awaiting response from the server for unencrypted communication or encrypted communication"""
    data_recived = s.recv(1024)
    decoded_response_from_server = data_recived.decode("utf-8")
    
    if len(decoded_response_from_server.strip("()")) == 2:
        """If we only recive the CC packet from the server we will contiune with the unencrypted communication"""
        
        print(f"reciving response from server: {decoded_response_from_server}")

    if len(decoded_response_from_server.strip("()")) > 2:
        """" Now if the communication is encrypted then we have to first recive the Confirm-Connection-Packet and then send out the Encryption-Packet"""        
        print(f"reciving connection packet from server: {decoded_response_from_server}")
        
        decoded_servers_public_key = rsa_public_key_converter(decoded_response_from_server)
        
        

main()