#!/usr/bin/python3

import sys
import socket
import select
import json
import base64
import csv
import random
from common_comm import send_dict, recv_dict, sendrecv_dict

from Crypto.Cipher import AES

# Dicionário com a informação relativa aos clientes
users = {}

# return the client_id of a socket or None
def find_client_id (client_sock):
	return None


# Função para encriptar valores a enviar em formato json com codificação base64
# return int data encrypted in a 16 bytes binary string and coded base64
def encrypt_intvalue (client_id, data):
	return None


# Função para desencriptar valores recebidos em formato json com codificação base64
# return int data decrypted from a 16 bytes binary string and coded base64
def decrypt_intvalue (client_id, data):
	return None


# Incomming message structure:
# { op = "START", client_id, [cipher] }
# { op = "QUIT" }
# { op = "NUMBER", number }
# { op = "STOP" }
#
# Outcomming message structure:
# { op = "START", status }
# { op = "QUIT" , status }
# { op = "NUMBER", status }
# { op = "STOP", status, min, max }


#
# Suporte de descodificação da operação pretendida pelo cliente
#
def new_msg (client_sock):
	return None
# read the client request
# detect the operation requested by the client
# execute the operation and obtain the response (consider also operations not available)
# send the response to the client


#
# Suporte da criação de um novo jogador - operação START
#
def new_client (client_sock, request):
	return None
# detect the client in the request
# verify the appropriate conditions for executing this operation
# process the client in the dictionary
# return response message with or without error message


#
# Suporte da eliminação de um cliente
#
def clean_client (client_sock):
	return None
# obtain the client_id from his socket and delete from the dictionary


#
# Suporte do pedido de desistência de um cliente - operação QUIT
#
def quit_client (client_sock, request):
	return None
# obtain the client_id from his socket
# verify the appropriate conditions for executing this operation
# process the report file with the QUIT result
# eliminate client from dictionary
# return response message with or without error message


#
# Suporte da criação de um ficheiro csv com o respectivo cabeçalho
#
def create_file ():
	return None
# create report csv file with header


#
# Suporte da actualização de um ficheiro csv com a informação do cliente e resultado
#
def update_file (client_id, result):
	return None
# update report csv file with the result from the client


#
# Suporte do processamento do número de um cliente - operação NUMBER
#
def number_client (client_sock, request):
	return None
# obtain the client_id from his socket
# verify the appropriate conditions for executing this operation
# return response message with or without error message


#
# Suporte do pedido de terminação de um cliente - operação STOP
#
def stop_client (client_sock, request):
	return None
# obtain the client_id from his socket
# verify the appropriate conditions for executing this operation
# process the report file with the result
# eliminate client from dictionary
# return response message with result or error message

def main():
    # validate the number of arguments and eventually print error message and exit with error
    # verify type of of arguments and eventually print error message and exit with error
    if len(sys.argv) != 2:
        print("Numero de argumentos invalido\nUso:python3 server.py <porto>")
        sys.exit(1)
    try:
        port = int(sys.argv[1])
        if port <= 0:
            print("Porto tem de ser maior que 0")
            sys.exit(2)
    except ValueError:
        print("Porto tem de ser um valor inteiro")
        sys.exit(2)
    print_info("A iniciar o servidor")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(10)
    clients = []
    try:
        create_file()
    except OSError:
        print_info("Erro ao criar o ficheiro")
        return None
    print_info("Servidor iniciado")
    while True:
        try:
            available = select.select([server_socket] + clients, [], [])[0]
        except ValueError:
            # Sockets may have been closed, check for that
            for client_sock in clients:
                if client_sock.fileno() == -1:
                    clients.remove(client_sock)  # closed
                continue  # Reiterate select
        for client_sock in available:
            # New client?
            if client_sock is server_socket:
                newclient, addr = server_socket.accept()
                clients.append(newclient)
            # Or an existing client
            else:
                try:
                    # See if client sent a message
                    if len(client_sock.recv(1, socket.MSG_PEEK)) != 0:
                        # client socket has a message
                        # print ("server" + str (client_sock))
                        new_msg(client_sock)
                    else:  # Or just disconnected
                        clients.remove(client_sock)
                        clean_client(client_sock)
                        client_sock.close()
                        break  # Reiterate select
                except:
                    print_info("Um cliente saiu inesperadamente")
                    clients.remove(client_sock)
                    clean_client(client_sock)
                    client_sock.close()
                    break  # Reiterate select
if __name__ == "__main__":
    main()