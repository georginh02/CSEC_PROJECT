import socket
from client_prompting import user_commands 
from packets import start_packet , packet_formatter ,  ec_packet
from helpers import rsa_public_key_converter 


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.gethostname()
    port = 8081

    s.connect((host, port))
    
    #-----------------------------------------
    # step 2
    
    # Sending intitial setup packet to server / calling the packet formatter and the start paket as the inital message 
    initial_message = packet_formatter(start_packet())
    print(f"sending {initial_message} packet to server...")
    s.send(initial_message.encode("utf-8"))
    
    #-----------------------------------------
    # step 8
    
    # Awaiting response from the server for unencrypted communication or encrypted communication
    data_recived = s.recv(1024)
    decoded_response_from_server = data_recived.decode("utf-8")
    
    
    # What we are checking here is if we get the (CC) paket all we do is strip () and check if the length of the decoded_response_from_server response is equal to then we recived a CC paket
    if len(decoded_response_from_server.strip("()")) == 2: 
        
        #If we only recive the CC packet from the server we will contiune with the unencrypted communication and that is it
        print(f"reciving response from server: {decoded_response_from_server}")

    # same logic as the first if statement but now we are just checking for if the length is greater than 2 
    if len(decoded_response_from_server.strip("()")) > 2:
        
        # Now if the communication is encrypted then we have to first recive the Confirm-Connection-Packet and then send out the Encryption-Packet       
        print(f"reciving connection packet from server: {decoded_response_from_server}")
        
        # use the rsa_public_key_converter to remove all unessecary data and just get the proper formatted servers public key
        decoded_servers_public_key = rsa_public_key_converter(decoded_response_from_server) # step 9 call the rsa key converter to get the proper rsa_public key and make it into a string
        
        # send the decoded_servers_public_key into the ec_packet function so it can make the paket to send back to the server
        complete_ec_packet = ec_packet(decoded_servers_public_key) # Step 10 mentioned in pakets
        s.send(complete_ec_packet.encode("utf-8")) # step 11 we send the ec packet
        print(f"sending ec packet to server {complete_ec_packet}")
        
    #-----------------------------------------
    count = 0 
    try:  
        while True:
            user_choice = user_commands()
            if isinstance(user_choice , list):
                for paket in user_choice:
                    s.send(paket.encode("utf-8"))
                    print(f"sending packet to server (openwrite): {paket}")
            else:   
                s.send(user_choice.encode("utf-8"))
                print(f"sending users choice and complete cm packet to server: {user_choice}")
                
            packet_recived = s.recv(1024)
            decoded_packet_from_server = packet_recived.decode("utf-8")
            
            if decoded_packet_from_server.strip("()").startswith("EE"):
                count += 1
                if count < 2:
                    print(f"this is your {count} exception reporting to server...")
                    print(f"issue {decoded_packet_from_server}")
                    print("pls note you only have 2 tries before connection gets closed automatically")
                else:
                    print("Error limit exceeded , closing connection...")
                    print("sending notice to server that client decided to end conversation")
                    end_packet = "(End)"
                    s.send(end_packet.encode("utf-8"))
                    s.close()
                    break  
                
            elif decoded_packet_from_server.strip("()").startswith("SC"):
                print(f"recived sucessful packet from server: {decoded_packet_from_server}..")
            else:
                if "(SC)" in decoded_packet_from_server:
                    text_part, seperator , after  = decoded_packet_from_server.partition("(SC)")
                    print(f"recived the text packet from server: {text_part}")
                    print(f"recived sucessful packet from server: {seperator}...")
               
            
            
    except KeyboardInterrupt:           
        print("client ended the connection by cntrl-c ")
        end_packet = "(End)"
        s.send(end_packet.encode("utf-8"))
        print(f"Sent {end_packet} packet to server")
        s.close()
main()