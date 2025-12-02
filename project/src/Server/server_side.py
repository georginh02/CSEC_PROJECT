import socket
import os, sys, stat
import threading
from checks import is_secure
from decryption import decrypt_ec_packet
from packets import not_secure_packet , secure_connection_packet
from helpers import execute_user_commands , openread_check , openwrite_check
import os

class myThread(threading.Thread):
    def __init__(self, s , add):
        threading.Thread.__init__(self)
        self.sock = s
        self.add = add
    
    def run(self):
        self.chatting()

    def chatting(self):
        print("Connection from %s" % str(self.add))
        
        # recive the setup packet from the client side
        data_recived = self.sock.recv(1024)
        decoded_setup_packet = data_recived.decode("utf-8")
        print(f"recived {decoded_setup_packet} from client")

        if is_secure(decoded_setup_packet):
            sending_secure_connection_packet = self.sock.send(secure_connection_packet().encode("utf-8"))
            print(f"sending secure Confirm-Connection-Packet to client {sending_secure_connection_packet}...")
            
        # waiting for an ec packet from the server
            recived_ec_packet = self.sock.recv(1024)
            decoded_ec_packet = recived_ec_packet.decode("utf-8")
            print(f"recived ec packet from client.. \n {decoded_ec_packet}")
            
            # calling the decrypt_ec_packet to get the algorithm session id and public key of the server
            decrypt_ec_packet(decoded_ec_packet)
            
        else:
            na_secure_packet = self.sock.send(not_secure_packet().encode("utf-8"))
            print(f"Sending {na_secure_packet} packet(s) to client as connection will not be encrypted")     
            
        while True:
            user_commands = self.sock.recv(1024)
            decoded_user_commands = user_commands.decode("utf-8")
            print(f"recived {decoded_user_commands} from client")
            
            if decoded_user_commands[4:12] == "openRead":
                openread_check(self.sock , decoded_user_commands)
                continue
            
            if decoded_user_commands[4:13] == "openWrite":
                dm_packet = self.sock.recv(4096)  
                decoded_dm_packet = dm_packet.decode("utf-8")
                print(f"recived dp packet from client {decoded_dm_packet}")
                
                openwrite_check(self.sock, decoded_user_commands, decoded_dm_packet)
                continue
            
            
            output = execute_user_commands(decoded_user_commands)
    
            if output:
                sc = "(SC)"
                print(output)
                self.sock.send(sc.encode("utf-8"))
            else:
                ee = "(EE)"
                self.sock.send(ee.encode("utf-8"))
            
            if decoded_user_commands.strip("()").startswith("EE"):
                print("server has been notified that client raised an exception packet (EE)")
            elif decoded_user_commands.strip("()").startswith("End"):
                print("bye client")
                self.sock.close()
                break
            
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 8081
serversocket.bind((host, port))
serversocket.listen(5)

while True:
    clientsocket, addr = serversocket.accept()
    t1 = myThread(clientsocket, addr)
    t1.start()