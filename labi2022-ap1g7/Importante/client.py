from os import CLD_CONTINUED
import socket
import json
import string
import sys
from common_comm import send_dict, recv_dict, sendrecv_dict

def run_client(client_id, port, host):
    #create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, 0))
    #connect to server
    s.connect ((host, port))

    while 1:
        operation = input("Operation (START/QUIT): ")
        if(type(operation)== 'str' ):
            if(operation.lower() == "start"):
                start_request = { "op": "START", "client_id": client_id }
                msg = sendrecv_dict(s, start_request)
                
                if(msg['op']== "START"): 
                    if(msg['status']== False):
                        print(msg['error'])
                        sys.exit(0)

                while 1:
                    number = input("-> ")
                    if(type(number)== 'str' and number.lower() == "stop"):
                        stop_request = { "op": "STOP" }
                        response = sendrecv_dict (s, stop_request)
                        if(response['op']== "STOP"): 
                            if(response['status']== False):
                                print(response['error'])
                                sys.exit(0)
                            else:
                                print("min: " + response['min'] + " max: " + response['max'])

                                
                    else:
                        number_request = { "op": "NUMBER", "number": number }
                        response = sendrecv_dict (s, number_request)

                        if(response['op']== "NUMBER"): 
                            if(response['status']== False):
                                print(response['error'])
                                sys.exit(0)

def main():
    client_id = sys.argv[1]
    port = sys.agrv[2]
    host = sys.argv[3]

    

    while():
        run_client(client_id, port, host)
