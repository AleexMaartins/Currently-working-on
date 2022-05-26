#!/usr/bin/python3

import os
import sys
import socket
import json
import base64
from common_comm import send_dict, recv_dict, sendrecv_dict
from Crypto.Cipher import AES


# Função para encriptar valores a enviar em formato jsos com codificação base64
# return int data encrypted in a 16 bytes binary string coded in base64
def encrypt_intvalue(cipherkey, data):
    # Igual ao servidor
    # Se não pretender usar encriptação simplesmente devolve o valor dado
    if cipherkey == None:
        return int(data)
    cipher = AES.new(cipherkey, AES.MODE_ECB)
    data = cipher.encrypt(bytes("%16d" % (data), "utf-8"))
    data_tosend = str(base64.b64encode(data), "utf-8")
    return data_tosend


# Função para desencriptar valores recebidos em formato json com codificação base64
# return int data decrypted from a 16 bytes binary strings coded in base64
def decrypt_intvalue(cipherkey, data):
    if cipherkey == None:
        return int(data)
    cipher = AES.new(cipherkey, AES.MODE_ECB)
    data = base64.b64decode(data)
    data = cipher.decrypt(data)
    data = int(str(data, "utf-8"))
    return data


# verify if response from server is valid or is an error message and act accordingly
def validate_response(client_sock, response):
    status = response["status"]
    if status == False:
        print(response["error"])
        client_sock.close()
        sys.exit(3)
    return None


# Informa o servidor que um novo cliente está a tentar fazer conexão
# Retorna o maximo de tentativas
def new_client(client_sock, client_id, cipher_key):
    key = cipher_key
    if cipher_key != None:
        key = str(base64.b64encode(cipher_key), "utf-8")
    msg = {
        "op": "START",
        "client_id": client_id,
        "cipher": key
    }
    s_msg = sendrecv_dict(client_sock, msg)
    validate_response(client_sock, s_msg)
    max_attempts = decrypt_intvalue(cipher_key, s_msg["max_attempts"])
    return max_attempts


# process QUIT operation
def quit_action(client_sock):
    msg = {
        "op": "QUIT"
    }
    s_msg = sendrecv_dict(client_sock, msg)
    validate_response(client_sock, s_msg)
    print("Obrigado por usar o nosso software!")
    client_sock.close()
    sys.exit(4)

def stop(client_sock, cipher):
    msg = {
        "op": "STOP",
    }
    s_msg = sendrecv_dict(client_sock, msg)
    validate_response(client_sock, s_msg)
    print("Obrigado por usar o nosso software!")
    return True
# Outcomming message structure:
# { op = "START", client_id, [cipher] }
# { op = "QUIT" }
# { op = "NUMBER", number }
# { op = "STOP" }
#
# Incomming message structure:
# { op = "START", status }
# { op = "QUIT" , status }
# { op = "NUMBER", status }
# { op = "STOP", status, min, max }


#
# Suporte da execução do cliente
#
def run_client(client_sock, client_id):
    cipher_key = cipher()
    max = 0;
    min;
    print("\n Valores inteiros a adicionar para a lista: ")
    print("Caso queira parar de adicionar valores e receber os valores do minimo e maximo da lista: stop")
    print("Caso queira sair do programa: quit")
    
    while True:
        resposta = input("->")
        if resposta.lower() == "quit":
            quit_action(client_sock)
            return None
        elif resposta.lower() == "stop":
            if max == 0: #verificar na linha 112 se a lista está vazia
                quit_action(client_sock)
                return None
            else:
                stop(client_sock, cipher_key)
                return None
        else:
            try:
                value = int(resposta)
                min = value;
                if value<min:
                        
            except ValueError:
                print("Valor deve ser um número inteiro")


# Pergunta ao utilizador se dejesa usar encriptacao
# Retorna None caso nao queira e uma cypher key caso queira
def cipher():
    response = ""
    while response.lower() != "s" and response.lower() != "n":
        response = input("Deseja comunicar com encriptacao? (S/N) ->")
    if response.lower() == "n":
        return None
    if response.lower() == "s":
        return os.urandom(16)
        

def main():
    # validate the number of arguments and eventually print error message and exit with error
    # verify type of of arguments and eventually print error message and exit with error
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Erro. Numero errado de argumentos.")
        print("Uso: python3 client.py <client id> <porto> [maquina]")
        sys.exit(1)
    try:
        port = int(sys.argv[2])
        if port <= 0:
            print("Porto tem de ser maior que 0")
            sys.exit(1)
    except ValueError:
        print("Porto tem de ser um valor inteiro")
        sys.exit(2)
    hostname = "127.0.0.1" 
    if len(sys.argv) == 4:
        ip = sys.argv[3].split(".")
        if len(ip) != 4:
            print("ERRO. O ip deve ser do tipo X.X.X.X")
            sys.exit(1)
        if int(ip[0]) <= 0 or int(ip[0]) > 255:
            print("ERRO. O primeiro octeto deve estar entre ]0 , 255]")
            sys.exit(1)
        if int(ip[1]) < 0 or int(ip[1]) > 255 or int(ip[2]) < 0 or int(ip[2]) > 255:
            print(
                "ERRO. O segundo e terceiro octeto devem estar entre [0 , 255]")
            sys.exit(1)
        if int(ip[3]) <= 0 or int(ip[3]) >= 255:
            print("ERRO. O ultimo octeto deve estar entre ]0 e 255[")
            sys.exit(1)
        hostname = ip
    print("A tentar conectar ao servidor")
    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((hostname, port))
    except:
        print("Ocorreu um erro ao conectar ao servidor")
        print("Certifique-se que o ip e o porto estão corretos")
        sys.exit(1)
    print("conectado")
    run_client(client_sock, sys.argv[1])
    client_sock.close()
    sys.exit(0)


if __name__ == "__main__":
    main()