#!/usr/bin/python3

import sys
import socket
import select
import json
from Crypto.Util import Counter
from Crypto.Util.number import bytes_to_long
import base64
import csv
import random
import ast
from common_comm import send_dict, recv_dict, sendrecv_dict

from Crypto.Cipher import AES

# Dicionário com a informação relativa aos clientes
users = {}

# return the client_id of a socket or None
def find_client_id (client_sock):
	o = 0
	d = 0
	for i in users:

		if users["socket"] == str (client_sock):
			o = 1
			f = users["Nome"]
			
		break
	if o == 1:
		return f
	else:
		return None



# Função para encriptar valores a enviar em formato json com codificação base64
# return int data encrypted in a 16 bytes binary string and coded base64



# Função para desencriptar valores recebidos em formato json com codificação base64
# return int data decrypted from a 16 bytes binary string and coded base64



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
		s = recv_dict(client_sock)
		st = s["Dados"]
		if "op" in st :
			new_client (client_sock, st)
		
	
		

		return None
# read the client request
# detect the operation requested by the client
# execute the operation and obtain the response (consider also operations not available)
# send the response to the client


#
# Suporte da criação de um novo jogador - operação START
#
def new_client (client_sock, request):
	if request != None:
		cipher = base64.b64decode (request["cipher"])
		id = request["ID"]
		status = "Success"
		for i in users:
				if users["Nome"] == id:
					status = "False"
				break
		if status == "False":
				data = {"op" : "START", "status" : status, "Error": "Utilizador já existe"}
		else:
				c = str (client_sock)
				list = {"Nome" : str(id), "socket": c , "cipher": cipher, "numbers": [] }
				users.update(list)

			
				data = {"op" : "START", "status" : status}
	

		send_dict(client_sock, data)
		return None
	else:
		return None
# detect the client in the request
# verify the appropriate conditions for executing this operation
# process the client in the dictionary
# return response message with or without error message


#
# Suporte da eliminação de um cliente
#

# obtain the client_id from his socket and delete from the dictionary


#
# Suporte do pedido de desistência de um cliente - operação QUIT
#

# obtain the client_id from his socket
# verify the appropriate conditions for executing this operation
# process the report file with the QUIT result
# eliminate client from dictionary
# return response message with or without error message


#
# Suporte da criação de um ficheiro csv com o respectivo cabeçalho
#

# create report csv file with header


#
# Suporte da actualização de um ficheiro csv com a informação do cliente e resultado
#

# update report csv file with the result from the client


#
# Suporte do processamento do número de um cliente - operação NUMBER
#

     
# obtain the client_id from his socket
# verify the appropriate conditions for executing this operation
# return response message with or without error message


#
# Suporte do pedido de terminação de um cliente - operação STOP
#

# obtain the client_id from his socket
# verify the appropriate conditions for executing this operation
# process the report file with the result
# eliminate client from dictionary
# return response message with result or error message


def main():
	# validate the number of arguments and eventually print error message and exit with error
	# verify type of of arguments and eventually print error message and exit with error
	
	port = 5005

	server_socket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind (("127.0.0.1", port))
	server_socket.listen (10)

	clients = []
	create_file ()
	server_socket.listen ()

	while True:
		try:
			available = select.select ([server_socket] + clients, [], [])[0]
		except ValueError:
			# Sockets may have been closed, check for that
			for client_sock in clients:
				if client_sock.fileno () == -1: client_sock.remove (client) # closed
			continue # Reiterate select

		for client_sock in available:
			# New client?
			if client_sock is server_socket:
				newclient, addr = server_socket.accept ()
				clients.append (newclient)
				
			# Or an existing client
			else:
				# See if client sent a message
					if len (client_sock.recv (1, socket.MSG_PEEK)) != 0:
						# client socket has a message
						##print ("server" + str (client_sock))

						new_msg (client_sock)
					
							
					else: # Or just disconnected
							clients.remove (client_sock)
							clean_client (client_sock)
							client_sock.close ()
							break # Reiterate select

if __name__ == "__main__":
	main()
