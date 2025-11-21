import socket
import os, sys, stat
import threading
from checks import is_secure
from packets import not_secure_packet
from packets import secure_connection_packet

class myThread(threading.Thread):
    def __init__(self, s , add):
        threading.Thread.__init__(self)
        self.sock = s
        self.add = add
    
    def run(self):
        self.chatting()

    def chatting(self):
        print("Connection from %s" % str(self.add))
        
        """recive the setup packet from the client side"""
        data_recived = self.sock.recv(1024)
        decoded_setup_packet = data_recived.decode("utf-8")
        print(f"recived {decoded_setup_packet} from client")

        
        if is_secure(decoded_setup_packet):
            sending_secure_connection_packet = self.sock.send(secure_connection_packet().encode("utf-8"))
            print(f"sending secure Confirm-Connection-Packet to client {sending_secure_connection_packet}...")
        else:
            na_secure_packet = self.sock.send(not_secure_packet().encode("utf-8"))
            print(f"Sending {na_secure_packet} packet(s) to client as connection will not be encrypted")   

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 8083
serversocket.bind((host, port))
serversocket.listen(5)

while True:
    clientsocket, addr = serversocket.accept()
    t1 = myThread(clientsocket, addr)
    t1.start()