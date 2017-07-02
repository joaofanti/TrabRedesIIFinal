import json
import socket
import netifaces as ni

import sys
sys.path.insert(0, "Modelos")
sys.path.insert(0, "Modelos/Mapa")

from Game import *
from MapFactory import *
from UDPConnection import *
from time import gmtime, strftime

"""
    Representa um servidor MUD.
"""
class Servidor(UDPConnection):

    # Propriedades do servidor
    ConnectedClients = {}   # Dicionario de clientes conectados
    TextoAjuda = ""         # Texto a ser enviado como resposta da acao "Ajuda"

    # Lista de comandos
    _CMD_NOVA_CONEXAO = "CriaConexao"
    _CMD_EXAMINAR = "Examinar"
    _CMD_MOVER = "Mover"
    _CMD_PEGAR = "Pegar"
    _CMD_LARGAR = "Largar"
    _CMD_INVENTORIO = "Inventorio"
    _CMD_USAR = "Usar"
    _CMD_FALAR = "Falar"
    _CMD_COCHICHAR = "Cochichar"
    _CMD_AJUDA = "Ajuda"

    """
        Define um comando.
    """
    class Command:

        """
            Cria uma nova instancia de comando a partir da mensagem "<playerId>|<cmd> {parameters}"
        """
        def __init__(self, msg):

            msgSplit = msg.split('|')

            self.PlayerID = msgSplit[0]
            cmdAux = msgSplit[1].split(' ')

            self.Cmd = cmdAux[0]
            self.Parameters = []
            for i in range(1, len(cmdAux)):
                self.Parameters.append(cmdAux[i])
                

    """
        Inicializa uma nova instancia de MUD SERVER
    """
    def __init__(self, ip, porta):
        self.ConnectedClients = {}
        UDPConnection.__init__(self, ip, porta, 'server')
        self._Quantidade_Players = 0
        
        # Le o texto para resposta do comando 'Ajuda'
        with open('Recursos/Ajuda.txt', 'r') as data_file:
        	self.TextoAjuda = data_file.read()

        fct = MapFactory()
    	with open('Recursos/Mapa.txt', 'r') as data_file:
            jsonFormatted = json.load(data_file)
            with open('Recursos/MapaDesign.txt', 'r') as mapDesign:
                generatedMap = fct.GenerateMap(jsonFormatted, mapDesign.read())
                self.GameLogic = Game(generatedMap)

    """
        Escuta os dados recebidos pelo socket e executa a logica num laco infinito
    """
    def atualiza(self):

        # Recebe os dados pelo socket
        self.Buffer, endereco = self.Socket.recvfrom(self.BuffSize)

        # Remove o header da mensagem. TODO: Verificar por que tem que fazer isso.
        self.Buffer = self.Buffer[20:len(self.Buffer)]
        
        # Se a mensagem comeca com 'game' entao eh uma das mensagens do jogo
        if (self.Buffer.startswith(self.GameID)):
            self.Buffer = self.Buffer[len(self.GameID):]

            try:
                # Faz o parse dos dados para um comando valido
                cmd = self.Command(self.Buffer)

                # Se nao for uma mensagem propria (por causa do UDP) continua o processamento
                if (cmd.PlayerID != self.ID):
                    print ">> O jogador " + cmd.PlayerID + " solicitou o comando " + cmd.Cmd
                    reply = ""

                    if (cmd.Cmd == self._CMD_NOVA_CONEXAO):
                        reply = self.GameLogic.CriaJogador(cmd.PlayerID, endereco[0])
                    elif (cmd.Cmd == self._CMD_AJUDA):
                        reply = self.TextoAjuda
                    elif (cmd.Cmd == self._CMD_EXAMINAR):
                        reply = self.GameLogic.Examina(cmd.PlayerID)
                    elif (cmd.Cmd == self._CMD_MOVER):
                        reply = self.GameLogic.Move(cmd.PlayerID, cmd.Parameters[0])
                    elif (cmd.Cmd == self._CMD_INVENTORIO):
                        reply = self.GameLogic.LeInventorio(cmd.PlayerID)
                    elif (cmd.Cmd == self._CMD_USAR):
                        if (len(cmd.Parameters) > 1):
                            reply = self.GameLogic.UsaItem(cmd.PlayerID, cmd.Parameters[0], cmd.Parameters[1])
                        else:
                            reply = self.GameLogic.UsaItem(cmd.PlayerID, cmd.Parameters[0])
                    else:
                        reply = "Comando nao eh valido."

                    self.sendMsg(reply, endereco[0])

            except Exception as ex:
                print "Ocorreu um erro ao executar o comando ", self.Buffer, "\n-> Erro:", ex
                self.sendMsg("Ocorreu um erro ao executar o comando", endereco[0])

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
    servidor = Servidor(ip, 5005)
    print "Servidor MUD inicializado com sucesso em ", servidor.IP, " [", servidor.Port, "] "

    # Deixa o servidor rodando infinitamente
    while True:
        servidor.atualiza()
