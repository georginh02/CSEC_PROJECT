import socket
from packets import start_packet
from packets import packet_formatter

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = "127.0.0.1"
    port = 46868

    s.connect((host, port))

    """Sending intitial setup packet to server"""
    initial_message = packet_formatter(start_packet())
    print(f"sending {initial_message} packet to server")
    s.send(initial_message.encode("utf-8"))

    """Awaiting response from the server wheter or not to use encrypted or non encrypted comms"""
    data_recived = s.recv(1024)
    decoded_response_from_server = data_recived.decode("utf-8")
    print(f"reciving response from server: {decoded_response_from_server} packet")

main()