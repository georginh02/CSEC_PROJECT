from config import absolute_dir , executable , root_dir
import subprocess

def execute_user_commands(command: str) -> str: 
    try:
        
        complete_command = subprocess.run(
            [executable , root_dir , command.strip() ] , capture_output= True ,  text= True
            )
        return complete_command.stdout.strip()
    
    except Exception as e:
            print(f"Error {e}")