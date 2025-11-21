from session import session_generator , random_number

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
    user_input = input("what type of encryption do you want Aes or Caeser: ")
    if user_input.lower()== "aes":
        return session_generator()
    elif user_input.lower() == "caeser":
        return random_number()
    else:
         print("pls enter a proper option")
         encryption_choice() 
         
