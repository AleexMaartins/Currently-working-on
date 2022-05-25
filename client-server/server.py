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
# Nome do ficheiro com a informação do jogo
f_name = "report.csv"
# Cabeçalho do ficheiro csv
header = ["cliente", "lista",
          "maximo", "minimo"]
# Compara o socket de cada cliente em users com o socket dado em parâmetro
# return the client_id of a socket or None
def find_client_id(client_sock):
    for client in users:
        if users[client]["socket"] == client_sock:
            return client
    return None
# Função para encriptar valores a enviar em formato json com codificação base64
# return int data encrypted in a 16 bytes binary string and coded base64
def encrypt_intvalue(client_cipher, data):
    # O cliente não pretende usar encriptação
    # Isto evita ter de verificar se é para encriptar todas as vezes que o servidor manda
    # um valor numérico
    if client_cipher == None:
        return int(data)
    # O cliente pretende usar encriptação
    cipher = AES.new(client_cipher, AES.MODE_ECB)
    data = cipher.encrypt(bytes("%16d" % (data), "utf-8"))
    data_tosend = str(base64.b64encode(data), "utf-8")
    return data_tosend
# Função para desencriptar valores recebidos em formato json com codificação base64
# return int data decrypted from a 16 bytes binary string and coded base64
def decrypt_intvalue(client_cipher, data):
    if client_cipher == None:
        return int(data)
    cipher = AES.new(client_cipher, AES.MODE_ECB)
    data = base64.b64decode(data)
    data = cipher.decrypt(data)
    data = int(str(data, "utf-8"))
    return data

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
def new_msg(client_sock):
    msg = recv_dict(client_sock)
    # É esperado que o cliente mande sempre um campo op na mensagem
    # Caso isso não acontece então o código do cliente tem erros
    op = msg["op"]
    if op == "START":
        new_client(client_sock, msg)
    elif op == "QUIT":
        quit_client(client_sock)
   
    elif op == "STOP":
        stop_client(client_sock, msg)
    else:
        # Não é suposto chegar aqui pois se chegar é porque o cliente tem erros
        print("Operacao desconhecida:" + op)
        msg = {
            "op": op,
            "status": False,
            "error": "operacao desconhecida"
        }
        send_dict(client_sock, msg)
# read the client request
# detect the operation requested by the client
# execute the operation and obtain the response (consider also operations not available)
# send the response to the client
#
# Suporte da criação de um novo jogador - operação START
#
def new_client(client_sock, request):
    client_id = request["client_id"]
    print("Cliente a tentar conectar: " + client_id)
    # Verifica se o cliente já existe
    if find_client_id(client_sock) != None:
        # Envia mensagem de erro a dizer que o client já existe
        msg = {
            "op": "START",
            "status": False,
            "error": "Cliente já existe"
        }
        print("Erro: Cliente já existe (Cliente: " + client_id + ")")
        send_msg(client_sock, msg)
        return None
    cipher = request["cipher"]
    if cipher != None:
        cipher = base64.b64decode(request["cipher"])
    # Gerar o número secreto e o máximo de tentativas
    secret_number = random.randint(0, 100)
    max_attempts = random.randint(10, 30)
    # Guardar o conteúdo deste cliente num dicionário
    content = {
        "socket": client_sock,
        "cipher": cipher,
        "guess": secret_number,
        "max_attempts": max_attempts,
        "attempts": 0
    }
    # Adicionar o cliente e o seu conteúdo ao dicionário de clientes
    users[client_id] = content
    # Enviar a mensagem de sucesso
    msg = {
        "op": "START",
        "status": True,
        "max_attempts": encrypt_intvalue(cipher, max_attempts)
    }
    send_msg(client_sock, msg)
    print("Cliente conectado com sucesso")
# detect the client in the request
# verify the appropriate conditions for executing this operation
# obtain the secret number and number of attempts
# process the client in the dictionary
# return response message with results or error message
#
# Suporte da eliminação de um cliente
# Devolve True ou False dependendo do sucesso da eliminação do cliente
def clean_client(client_sock):
    client = find_client_id(client_sock)
    if client != None:
        # Elimina o cliente do dicionário
        users.pop(client)
        print("Cliente removido com sucesso (Cliente: " + client + ")")
        return True
    return False
#
# Suporte do pedido de desistência de um cliente - operação QUIT
#
def quit_client(client_sock):
    client_id = find_client_id(client_sock)
    print("Cliente " + client_id + " pediu para sair")
    if client_id != None:
        # Envia mensagem de sucesso
        msg = {
            "op": "QUIT",
            "status": True
        }
        send_msg(client_sock, msg)
        client = users[client_id]
        attempts = client["attempts"]
        guess = client["guess"]
        max_attempts = client["max_attempts"]
        update_file(
            client_id, guess, max_attempts, attempts, "QUIT")
        clean_client(client_sock)
        print("Cliente " + client_id + " saiu com sucesso")
    else:
        # Cliente não está a jogar
        # Devolver mensagem a indicar o erro
        msg = {
            "op": "QUIT",
            "status": False,
            "error": "Cliente inexistente"
        }
        send_msg(client_sock, msg)
        print("Cliente nao saiu com sucesso. Causa: Cliente nao existe")
# Suporte da criação de um ficheiro csv com o respectivo cabeçalho
def create_file():
    print("A criar ficheiro csv")
    # Inicializa o ficheiro csv e escreve o cabeçalho
    file = open(f_name, "w")
    writer = csv.writer(file)
    writer.writerow(header)
    file.flush()
    file.close()
    print("Ficheiro criado com sucesso")
# Suporte da actualização de um ficheiro csv com a informação do cliente e resultado
def update_file(client_id, secret_number, max_attempts, attempts, result):
    try:
        print("A escrever dados de " + client_id + " para o ficheiro")
        # Abre em modo append para não sobrepor o ficheiro criado anteriormente em create_file
        file = open(f_name, "a")
        writer = csv.writer(file)
        line = [client_id, secret_number, max_attempts, attempts, result]
        writer.writerow(line)
        file.flush()
        file.close()
        print("Dados escritos com sucesso")
    except OSError:
        print("Erro ao escrever no ficheiro")
        print("linha -> " + client_id + " , " + secret_number +
                   " , " + max_attempts + " , " + attempts + " , " + result)


def number_client (client_sock, request):
	return None
# obtain the client_id from his socket
# verify the appropriate conditions for executing this operation
# return response message with or without error message


#
# Suporte do pedido de terminação de um cliente - operação STOP
#
def stop_client(client_sock, request):   #AINDA FALTA ACABAR
    client_id = find_client_id(client_sock)
    print("Cliente " + client_id + " pediu para terminar")
    # Cliente inexistente
    if client_id == None:
        msg = {
            "op": "QUIT",
            "status": False,
            "error": "Cliente inexistente"
        }
        send_msg(client_sock, msg)
        print("Pedido para terminar falhado. Causa: Cliente inexistente")
        return None
    client = users[client_id]
    # Número de jogadas registado pelo servidor
    cipher = client["cipher"]
    number = decrypt_intvalue(cipher, request["number"])
    client_attempts = decrypt_intvalue(cipher, request["attempts"])
    # Número de jogadas dado pelo cliente não é igual ao do servidor

# obtain the client_id from his socket
# verify the appropriate conditions for executing this operation
# process the report file with the result
# eliminate client from dictionary
# return response message with result or error message
def send_msg(client_sock, msg):
    sent = send_dict(client_sock, msg)
    if not sent:
        # DEBUG
        print("ERRO:mensagem nao enviada")

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
    print("A iniciar o servidor")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(10) 
    clients = []
    try:
        create_file()
    except OSError:
        print("Erro ao criar o ficheiro")
        return None
    print("Servidor iniciado")
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
                    print("O cliente saiu inesperadamente")
                    clients.remove(client_sock)
                    clean_client(client_sock)
                    client_sock.close()
                    break  # Reiterate select
if __name__ == "__main__":
    main()