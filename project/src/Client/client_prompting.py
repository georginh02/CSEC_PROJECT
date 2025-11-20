def encryption_type() -> int:
    "asks the client for the type of "
    start_packet_options= {
        "Non Secured RFMP v1.0": 0 ,
        "Secured RFMP v1.0" : 1
        }
    message = f"If you want to use {list(start_packet_options.keys())[0]} please enter 0 or please please enter 1 for {list(start_packet_options.keys())[1]}: "
    
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


