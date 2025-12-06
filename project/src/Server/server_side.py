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
        
        #-----------------------------------------
        # Step 3
        
        # recive the setup packet from the client side
        data_recived = self.sock.recv(1024)
        decoded_setup_packet = data_recived.decode("utf-8")
        print(f"recived {decoded_setup_packet} from client")
        
        #-----------------------------------------
        
        #-----------------------------------------
        # Step 5
        
        # if is_secure is true (encrypted) then we have to send a secure conneciton packet back to the client
        if is_secure(decoded_setup_packet):
            # if it is secure we call the secure_connection_packet (CC , server_rsa_publickey) and send it to the client step 7 for encrypted comms 
            sending_secure_connection_packet = self.sock.send(secure_connection_packet().encode("utf-8")) # step 7 is where we send the complete  (CC , server_rsa_publickey)
            print(f"sending secure Confirm-Connection-Packet to client {sending_secure_connection_packet}...")
            
            # waiting for an ec packet from the client once recived we then move on the the next step which is step 12
            recived_ec_packet = self.sock.recv(1024) # reciving the (EC, ALgorithm, session_key, username:Client_public_key) packet this is the start of step 12 for encrypted comms
            decoded_ec_packet = recived_ec_packet.decode("utf-8")
            print(f"recived ec packet from client.. \n {decoded_ec_packet}")
            
            # calling the decrypt_ec_packet to get the algorithm session id and public key of the client 
            print(decrypt_ec_packet(decoded_ec_packet)) # step 13 we need to decrypt the ec packet and thats it
            
        else:
            # if it is not secure then we just send a (CC) paket to the client by calling the not_secure_packet this marks the start of step 7 for non encrypted comms
            na_secure_packet = self.sock.send(not_secure_packet().encode("utf-8")) # step 7 for the non encrypted comms is where we just send the (CC) packet and do not listen for an (EC, ALgorithm, session_key, username:Client_public_key) from the client
            print(f"Sending {na_secure_packet} packet(s) to client as connection will not be encrypted")     
            
        #-----------------------------------------  
        # we make the while true loop to keep it going 
        while True:
            # recive comands from client
            user_commands = self.sock.recv(1024)
            decoded_user_commands = user_commands.decode("utf-8")
            print(f"recived {decoded_user_commands} from client")
            
            # check if here is checking for any (EE) pakets from the client
            if decoded_user_commands.strip("()").startswith("EE"):
                print("server has been notified that client raised an exception packet (EE)")
                
            # check if there is any (End) packets from the client
            elif decoded_user_commands.strip("()").startswith("End"):
                print("bye client")
                self.sock.close()
                break
            
            # if the client sends and openread command we call the openread check 
            if decoded_user_commands[4:12] == "openRead":
                openread_check(self.sock , decoded_user_commands)
                continue
            
            # if the client sends and openwrite we recive the cm packet first with the file then recive the wait for the dp packet and then call openwrite function 
            if decoded_user_commands[4:13] == "openWrite":
                dm_packet = self.sock.recv(4096)  
                decoded_dm_packet = dm_packet.decode("utf-8")
                print(f"recived dp packet from client {decoded_dm_packet}")
                
                openwrite_check(self.sock, decoded_user_commands, decoded_dm_packet)
                continue
            
            # for other system commands we just proceed as normal
            bool , output = execute_user_commands( decoded_user_commands)
            
            # so if its the function executed properly it will send an (SC) packet
            if bool:
                print(output)
                sc = "(SC)"
                print(f"sending {sc} packet to client...")
                self.sock.send(sc.encode("utf-8"))
                
            # if false it will send an (EE) packet to the client 
            else:
                print(output)
                ee = "(EE)"
                print(f"sending {ee} packet to client...")
                self.sock.send(ee.encode("utf-8"))
            
          
            
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname() # have to change this to "127.0.0.1" for the client in c to be able to connect
port = 8082
serversocket.bind((host, port))
serversocket.listen(5)

while True:
    clientsocket, addr = serversocket.accept()
    t1 = myThread(clientsocket, addr)
    t1.start()