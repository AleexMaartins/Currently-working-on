import socket
import json
import sys
from common_comm import send_dict, recv_dict, sendrecv_dict


def start(s, client_id):
    start_request = { "op": "START", "client_id": client_id }
    msg = sendrecv_dict(s, start_request)

    if(msg['status']== False):
        print(msg['error'])
        sys.exit(0)
    print("Server started successfully")
    return None
    
def number(s):
    number = int(input("number-> "))
    number_request = { "op": "NUMBER", "number": number }
    response = sendrecv_dict (s, number_request)

    if(response['status']== False):
        print(response['error'] + " Make sure to start the client first")
        return None
    
    print("Number added successfully")
    return None

def stop(s):
    stop_request = { "op": "STOP" }
    response = sendrecv_dict (s, stop_request)

    if(response['op']== "STOP"): 
        if(response['status']== False):
            msg = response['error']
            if(msg == "Inexistent Client\n"):
                print(msg + " Make sure to start the client first" )
            if(msg == "Insuficient Data\n"):
                print(msg + " Make sure to add numbers first" )
            return None
        else:
            print("min: " + str(response['min']) + " max: " + str(response['max']))
            return None

def quit(s):
    quit_request = { "op": "QUIT" }
    response = sendrecv_dict (s, quit_request)
    
    if(response['status']== False):
        print(response['error'] + " Make sure to start the client first")
        return None
    
    print("Client quitted successfully")
    s.close()
    sys.exit(0)
    
 

def run_client(client_id, port, host):
    #create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #connect to server
    s.connect ((host, port))
    print("Operations: START/NUMBER/STOP/QUIT\n")

    while 1:
        op = input("-> ").upper()
        
        if op == "START": 
            start(s, client_id)
        elif op == "NUMBER":
            number(s)
        elif op == "STOP":
            stop(s)
        elif op == "QUIT":
            quit(s)
        else: 
            print("Input a legit operation")
            continue

def valid_ip(address):
    try: 
        socket.inet_aton(address)
        return True
    except:
        return False

def main():
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Error.Wrong number of arguments.")
        print("Use: python3 client.py <client id> <port> [machine]")
        sys.exit(1)

    client_id = str(sys.argv[1])
    port = int(sys.argv[2])

    if port <= 0:
        print("Port must be bigger then 0")
        sys.exit(1)
    
    host = "127.0.0.1"
    if len(sys.argv) == 4:
        host = str(sys.argv[3])
        if not valid_ip(host):
            print("Invalid ip")
            sys.exit(1)


    run_client(client_id, port, host)

if __name__ == "__main__":
	main()
