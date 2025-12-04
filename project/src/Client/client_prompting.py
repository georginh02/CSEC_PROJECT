from packets import encrypt_data_if_secure

def user_commands() -> str:
    """ ths function just lists the available commands and allows the user to pick where we then format it into packets """
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