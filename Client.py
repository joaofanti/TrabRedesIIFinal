import socket
import thread
import netifaces as ni

import sys
sys.path.insert(0, "Modelos")
from UDPConnection import *

"""
    Representa um cliente do servidor MUD.
"""
class Client(UDPConnection):

    """
        Cria uma nova instancia de Client
    """
    def __init__(self,  mac, ip, port, interface, _id, serverIp):

        UDPConnection.__init__(self, mac, ip, port, interface)

        self.ID = _id
        self.ServerIP = serverIp
        self.ServerPort = 5005

        thread.start_new_thread(self.readLoop, ()) # Inicia a thread de leitura

        # Manda mensagem de conexao
        connectionMsg = self.createMsg(self.ID, 'CriaConexao')
        self.sendMsg(None, serverIp, self.ServerPort, connectionMsg)


    """
        Escuta os dados recebidos pelo socket e executa a logica num laco infinito
    """
    def readLoop(self):
        while True:
            rcvMsg = self.readMsg()
            if (rcvMsg != None):
                print '[SERVER]: {}'.format(rcvMsg["message"].split('|')[1])



# --------------------------------------------------

"""
    Metodo principal para rodar o cliente
"""
if __name__ == "__main__":

    # Pega o endereco IP lo (loopback) atual, geralmente 127.0.0.1
    ip = ni.ifaddresses("lo")[ni.AF_INET][0]['addr']

    # Para cada interface disponivel diferente da interface de loopback, verifica se seu endereco e IPv4 e, se for, salva-o na variavel IP
    for interface in ni.interfaces():
        try:
            ifIp = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
            if (ifIp != ip):
                ip = ifIp
                break
        except:
            continue

    # Coleta as informacoes do jogador
    port = input("Insira a porta para ser utilizada no socket (sugestao: 5006): ")
    playerName = raw_input("Insira o nome do jogador: ")
    
    # Tenta conectar o jogador no servidor
    client = None
    while True:
        serverIp = raw_input("Insira o endereco IP do servidor: ")

        # Valida o endereco IP
        try:
            socket.inet_aton(serverIp)
        except socket.error:
            print "Endereco IP nao e valido. Tente novamente.\n\n"
            continue

        try:
            print 'Iniciando conexao com o servidor..\n'
            client = Client(None, ip, port, interface, playerName, serverIp)
            break
        except Exception as ex:
            print ex
            print "Nao foi possivel estabelecer uma conexao com o servidor. Tente novamente.\n"

    while True:
        msg = raw_input()
        msg = client.createMsg(client.ID, msg)
        client.sendMsg(None, client.ServerIP, client.ServerPort, msg)