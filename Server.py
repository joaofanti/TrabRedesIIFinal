import re
import netifaces as ni

import sys
sys.path.insert(0, "Modelos")
sys.path.insert(0, "Modelos/Mapa")
from Game import *
from MapFactory import *
from UDPConnection import *

"""
    Representa um servidor MUD.
"""
class Server(UDPConnection):

    # Lista de comandos
    _CMD_CRIA_CONEXAO	= "CriaConexao"
    _CMD_INVENTORIO 	= "Inventorio"
    _CMD_COCHICHAR		= "Cochichar"
    _CMD_EXAMINAR		= "Examinar"
    _CMD_LARGAR			= "Largar"
    _CMD_FALAR			= "Falar"
    _CMD_MOVER			= "Mover"
    _CMD_PEGAR			= "Pegar"
    _CMD_AJUDA 			= "Ajuda"
    _CMD_USAR           = "Usar"
    _CMD_SAIR			= "Sair"

    """
        Define um cliente conectado.
    """
    class ConnectedClient:
        def __init__(self, mac, ip, port):
            self.MAC = mac
            self.IP = ip
            self.PORT = port

    """
        Define um comando.
    """
    class Command:

        """
            Cria uma nova instancia de comando a partir da mensagem "<playerId>|<cmd> {parameters}"
        """
        def __init__(self, msg):
			msg = re.findall(r"[\w']+", msg)

			self.GameID	= msg[0]
			self.PlayerID = msg[1]
			self.Action = msg[2]
			self.Parameters = []

			if (len(msg) > 3):
				for i in range(3, len(msg)):
					self.Parameters.append(msg[i])
                

    """
        Inicializa uma nova instancia de Server
    """
    def __init__(self,  mac, ip, port, interface):
        UDPConnection.__init__(self, mac, ip, port, interface)
        self.ID = 'server'
        self.Clients = []

        # Le o texto para resposta do comando 'Ajuda'
        with open('Recursos/Ajuda.txt', 'r') as data_file:
            self.TextoAjuda = data_file.read()

        # Gera o mapa
        fct = MapFactory()
        with open('Recursos/Mapa.txt', 'r') as data_file:
            jsonFormatted = json.load(data_file)
            with open('Recursos/MapaDesign.txt', 'r') as mapDesign:
                generatedMap = fct.GenerateMap(jsonFormatted, mapDesign.read())
                self.GameLogic = Game(generatedMap)

    """
        Deleta um cliente conectado.
    """
    def deleteClient(self, mac, ip, port):
        client = None
        for client in self.Clients:
            if client.MAC == mac and client.IP == ip and client.PORT == port:
                self.Clients.remove(client)
                return True
        return False

    """
        Envia mensagem para todos os clientes conectados.
    """
    def sendMsgToAll(self, msg):
        for client in self.Clients:
            self.sendMsg(client.MAC, client.IP, client.PORT, msg)

    """
        Escuta os dados recebidos pelo socket e executa a logica num laco infinito
    """
    def run(self):
    	while True:
            rcvMsg = self.readMsg()
            if (rcvMsg != None):
                cmd = self.Command(rcvMsg["message"])
                if (len(cmd.Parameters) > 0):
                    print '>> O jogador {} solicitou o comando {} {}'.format(cmd.PlayerID, cmd.Action, ' '.join(cmd.Parameters))
                else:
                    print '>> O jogador {} solicitou o comando {}'.format(cmd.PlayerID, cmd.Action)

                if (cmd.Action == self._CMD_CRIA_CONEXAO):
                    msg = self.GameLogic.CriaJogador(cmd.PlayerID, rcvMsg["source_ip"])
                    if (msg == "OK"):
                        newClient = self.ConnectedClient(rcvMsg["source_mac"], rcvMsg["source_ip"], rcvMsg["source_port"])
                        self.Clients.append(newClient)

                        msg = self.createMsg(self.ID, 'OK\n')
                        msg += 'Ola, {}\n'.format(cmd.PlayerID)
                        msg += 'Para jogar, escreva o comando desejado e tecle [ENTER]\n'
                        msg += 'Escreva o comando "Ajuda" para obter a lista completa de comandos.\n'
                        msg += 'Escreva o comando "Sair" para sair do jogo.\n'
                        self.sendMsg(rcvMsg["source_mac"], rcvMsg["source_ip"], rcvMsg["source_port"], msg)

                    else:
                        msg = self.createMsg(self.ID, 'Ja existe um usuario com o nickname {}'.format(cmd.PlayerID))
                        self.sendMsg(rcvMsg["source_mac"], rcvMsg["source_ip"], rcvMsg["source_port"], msg)

                elif (cmd.Action == self._CMD_AJUDA):
                    msg = self.createMsg(self.ID, self.TextoAjuda)
                    self.sendMsg(rcvMsg["source_mac"], rcvMsg["source_ip"], rcvMsg["source_port"], msg)

                elif (cmd.Action == self._CMD_MOVER):
                    msg = self.createMsg(self.ID, "O jogador {} moveu-se para '{}'".format(cmd.PlayerID, cmd.Parameters[0]))
                    self.sendMsgToAll(connectionMsg)

                elif (cmd.Action == self._CMD_SAIR):
                    msg = self.createMsg(self.ID, "O jogador {} saiu do jogo.".format(cmd.PlayerID))
                    self.sendMsgToAll(msg)
                    self.deleteClient(rcvMsg["source_mac"], rcvMsg["source_ip"], rcvMsg["source_port"])

                else:
                    msg = self.createMsg(self.ID, "Comando nao existente.")
                    self.sendMsg(rcvMsg["source_mac"], rcvMsg["source_ip"], rcvMsg["source_port"], msg)

# --------------------------------------------------

"""
    Metodo principal para rodar o servidor
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

    # Inicializa o servidor
    port = 5005
    servidor = Server(None, ip, port, interface)
    print "Servidor MUD inicializado com sucesso em ", servidor.IP, " [", servidor.Port, "] "

    # Deixa o servidor rodando infinitamente
    while True:
        servidor.run()
