from config import absolute_dir , executable , root_dir
from decryption import encrypt_data_if_secure_server , decrypt_data_if_secure_server
import subprocess
import os


    
def execute_user_commands( command: str) -> tuple[bool , str]: 
    global absolute_dir
    user_command = command.strip("()").split(",")
    stripped_command = user_command[2].strip()
    check_for_cd = stripped_command.split()
    working_dir = absolute_dir
    
    if check_for_cd[0].lower() == "cd":
        directory = check_for_cd[1]
        new_path = os.path.join(working_dir, directory)
        new_path = os.path.normpath(new_path)
        working_dir = new_path
        
        if os.path.isdir(working_dir):
            absolute_dir = new_path 
            return True , f"changed directory to: {working_dir}"
        return False , f"directory dosent exist : {working_dir}"
    
    try:
        complete_command = subprocess.run(
            [executable , root_dir, stripped_command ] , cwd=working_dir ,  capture_output= True ,  text = True 
            )
        output = complete_command.stdout.strip()
    
    except Exception as e:
            return False, str(e).strip()       

    if complete_command.returncode == 0:
        return  True , output 
    else:
        return False , output 
    
def openread_check(sock , user_command: str):
    file_path = os.path.join(absolute_dir , user_command[13:-1])
    successful_packet = "(SC)"
    try:
        with open(file_path, "r") as file:
            content = file.read()
            print(f"file content: {content}")
        payload = encrypt_data_if_secure_server(content)
        dp_packet = f"({payload})"
        sock.send(dp_packet.encode("utf-8"))
        print(f"sending response back to client (openread): {dp_packet}")

        successful_packet = "(SC)"
        sock.send(successful_packet.encode("utf-8"))
        print(f"sending success packet to client: {successful_packet}")
    except FileNotFoundError:
        # this is where the only exception can happen because if the file dosent exist then we will send an ee packet 
            print("Error: The file was not found.")
            ee = "(EE,404,File not found)"
            sock.send(ee.encode("utf-8"))   
                

def openwrite_check(sock , cm_packet: str , dm_packet: str):
    file = cm_packet[14:-1].strip()
    file_path = os.path.join(absolute_dir , file)
    payload = dm_packet[4:-1]
    successful_packet = "(SC)"
    
    text = decrypt_data_if_secure_server(payload)
    try:
        with open(file_path, "w") as file:
            file.write(text)
            print(f"Sucessfully wrote {text} to {file_path}")
            sock.send(successful_packet.encode("utf-8")) 
            print(f"sending sucess packet to server: {successful_packet}")
    except Exception as e:
        # i doubt there will be any errors here as write will just create the file anyways and write to it regardless but i will try to catch any exception possible (test)
            print(f"Error occured: {e}")
            ee = f"(EE,404,{e})"
            sock.send(ee.encode("utf-8"))  
            