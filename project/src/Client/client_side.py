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

    if initial_message.strip("()").endswith("0"):
        """Awaiting response from the server for unencrypted communication"""
        data_recived = s.recv(1024)
        decoded_response_from_server = data_recived.decode("utf-8")
        print(f"reciving response from server: {decoded_response_from_server}")

    """" Now if the communication is encrypted then we have to first recive the Confirm-Connection-Packet and then send out the Encryption-Packet"""
    if initial_message.strip("()").endswith("1"):
        recived_connection_packet = s.recv(1024)
        connection_packet_from_server = recived_connection_packet.decode("utf-8")
        print(f"reciving connection packet from server: {connection_packet_from_server} packet")
        
        decoded_servers_public_key = rsa_public_key_converter(connection_packet_from_server)
        
        

main()