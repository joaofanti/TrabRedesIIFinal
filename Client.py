import socket
import netifaces as ni

import sys
sys.path.insert(0, "Modelos")

from UDPConnection import *

class Cliente(UDPConnection):

    # Propriedades do cliente
    IPServidor = "0.0.0.0"  # IP do servidor para enviar mensagens

    """
        Cria uma nova instnacia de Cliente
    """
    def __init__(self, ip, porta, id, ipServer):

        # Inicializa
        self.IPServidor = ipServer
        UDPConnection.__init__(self, ip, porta, id)

        # Cria conexao com o servidor e aguarda resposta
        self.sendMsg("CriaConexao")
        if ("Jogador criado na sala inicial." not in self.Buffer):
            raise Exception(self.Buffer.split('|')[1])

    """
        Faz sobrecarga do "sendMsg" para que sempre se aguarde uma resposta.
    """
    def sendMsg(self, msg):
        super(Cliente, self).sendMsg(msg, self.IPServidor, True)

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
    nomeJogador = raw_input("Insira o nome do jogador: ")
    
    # Tenta conectar o jogador no servidor
    cliente = None
    while True:
        ipServidor = raw_input("Insira o endereco IP do servidor: ")

        # Valida o endereco IP
        try:
            socket.inet_aton(ipServidor)
        except socket.error:
            print "Endereco IP nao e valido. Tente novamente.\n\n"
            continue

        try:
            print 'Iniciando conexao com o servidor..'
            cliente = Cliente(ip, 5006, nomeJogador, ipServidor)
            break
        except:
            print "Nao foi possivel estabelecer uma conexao com o servidor. Tente novamente.\n\n"

    print "\n-----------------------------\n"
    print "Ola, " + nomeJogador
    print "Para jogar, digite um comando e pressione [ENTER]."
    print "Nota: digite o comando 'Ajuda' para obter a lista de todos os comandos do jogo.\n"

    while True:
        msg = raw_input("[CMD]: ")
        try:
            cliente.sendMsg(msg)
        except:
            print 'Ocorreu um erro: '
        print cliente.Buffer.split('|')[1], "\n"
        cliente.Buffer = ""
