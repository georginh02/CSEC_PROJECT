from packets import encrypt_data_if_secure

def encryption_type() -> int:
    """
    asks the client if they want encrypted communication or not
     
    Encrypted:
    - If the client selects number 1 then it the function will store number one 

    Non Encrypted:
    - 
    """
    start_packet_options= {
        "Non Secured RFMP v1.0": 0 ,
        "Secured RFMP v1.0" : 1
        }
    message = f"If you want to use {list(start_packet_options.keys())[0]} please enter 0 or please enter 1 for {list(start_packet_options.keys())[1]}: "
    
    try:
        user_inp = int(input(message))
    except Exception as e:
        print("Please enter either 0 or 1")
        return encryption_type()
    
    if user_inp not in start_packet_options.values() :
        print("Please enter either 0 or 1")
        return encryption_type()
    elif user_inp == 0:
        print(f"you have selected {list(start_packet_options.keys())[0]}")
        return start_packet_options["Non Secured RFMP v1.0"]
    else:
        print(f"you have selected {list(start_packet_options.keys())[1]}")
        return start_packet_options["Secured RFMP v1.0"]


def encryption_choice() -> str:
    user_input = input("what type of encryption do you want Aes or Caesar: ")
    if user_input.lower()== "aes":
        return user_input.lower()
    elif user_input.lower() == "caesar":
        return user_input.lower()
    else:
         print("pls enter a proper option")
         return encryption_choice() 
         

def user_commands() -> str:
    list_of_commands = [
        "mkdir", "cd", "rmdir", "del", "ren",
        "openRead", "openWrite",
        "dir", "whoami", "hostname", "systeminfo", "echo"
    ]

    print("Available commands:")
    print(list_of_commands)

    user_input = input("\nPlease pick a command from the list above: ").strip().lower()

    match user_input:
        
        case "mkdir":
            folder = input("Folder name: ")
            return f"(CM,prompt,mkdir {folder})"

        case "cd":
            path = input("Path to change into: ")
            return f"(CM,prompt,cd {path})"

        case "rmdir":
            folder = input("Folder name to remove: ")
            return f"(CM,prompt,rmdir {folder})"

        case "del":
            filename = input("File name to delete: ")
            return f"(CM,prompt,del {filename})"

        case "ren":
            old = input("Old name: ")
            new = input("New name: ")
            return f"(CM,prompt,ren {old} {new})"

        # OPEN / FILE HANDLING
        case "openread":
            filename = input("File to read: ")
            return f"(CM,openRead,{filename})"

        case "openwrite":
            filename = input("File to write to: ")
            content = input("Enter text to write into file: ")
            
            payload = encrypt_data_if_secure(content)
            
            return [
                f"(CM,openWrite,{filename})",
                f"(DP,{payload})"
            ]

        # ----------------------

        case "dir":
            return "(CM,prompt,dir)"

        case "whoami":
            return "(CM,prompt,whoami)"

        case "hostname":
            return "(CM,prompt,hostname)"

        case "systeminfo":
            return "(CM,prompt,systeminfo)"

        case "echo":
            text = input("Text to echo: ")
            return f"(CM,prompt,echo {text})"

        # ----------------------
        
        case _:
            print("Invalid command.")
            return user_commands()