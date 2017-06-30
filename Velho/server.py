from time import gmtime, strftime
import socket
import netifaces as ni
from udpConnection import UDPConnection

"""
    Representa um servidor MUD.
"""
class Servidor(UDPConnection):

    # Propriedades do servidor
    ConnectedClients = {}   # Dicionario de clientes conectados

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
        Inicializa uma nova instancia de MUD SERVER
    """
    def __init__(self, ip, porta):
        self.ConnectedClients = {}
        UDPConnection.__init__(self, ip, porta, 'server')

    """
        Escuta os dados recebidos pelo socket e executa a logica num laco infinito
    """
    def atualiza(self):

        # Recebe os dados pelo socket
        self.Buffer, endereco = self.Socket.recvfrom(self.BuffSize)

        # Remove o header da mensagem
        self.Buffer = self.Buffer[20:len(self.Buffer)]
        
        # Se a mensagem comeca com 'game' entao eh uma das mensagens do jogo
        if (self.Buffer.startswith(self.GameID)):

            # Pega as informacoes da mensagem removendo o GameID
            mensagemSplit = self.Buffer[len(self.GameID):].split('|')
            idJogador = mensagemSplit[0]

            # Se nao for uma mensagem propria, continua o processamento
            if (idJogador != self.ID):
                try:
                    # Divide a mensagem por espacos
                    comando = mensagemSplit[1].split(' ')
                    # Valida qual acao foi solicitada
                    msgToSend = "A requisicao nao eh valida"
                    print ">> O jogador ", idJogador, " solicitou o comando ", comando[0]
                    if (comando[0] == self._CMD_NOVA_CONEXAO):
                        self.ConnectedClients[idJogador] = endereco[0]
                        msgToSend = "200"
                        print "Novo jogador conectado: ", idJogador, " (", endereco[0], ")"

                    if (comando[0] == self._CMD_AJUDA):
                        msgToSend = " >> Examinar [sala/objeto]\n"
                        msgToSend += "     Retorna a descricao da sala atual (sala) ou objeto mencionado.\n"
                        msgToSend += "     A descricao da sala tambem deve listar as salas adjacentes e suas respectivas direcoes, objetos e demais jogadores presentes no local.\n"
                        msgToSend += " >> Mover [N/S/L/O]\n"
                        msgToSend += "     O jogador deve mover-se para a direcao indicada (norte, sul, leste ou oeste).\n"
                        msgToSend += "     Ao entrar numa nova sala, o jogo deve executar automaticamente o comando 'examinar sala', que descreve o novo ambiente ao jogador.\n"
                        msgToSend += " >> Pegar [objeto]\n"
                        msgToSend += "     O jogador coleta um objeto que esta na sala atual.\n"
                        msgToSend += "     Alguns objetos nao podem ser coletados, como no caso de 'porta'.\n"
                        msgToSend += " >> Largar [objeto]\n"
                        msgToSend += "     O jogador larga um objeto que esta no seu inventorio, na sala atual.\n"
                        msgToSend += " >> Inventorio\n"
                        msgToSend += "     O jogo lista todos os objetos carregados atualmente pelo jogador.\n"
                        msgToSend += " >> Usar [objeto] {alvo}\n"
                        msgToSend += "     O jogador usa o objeto mencionado;\n"
                        msgToSend += "     Em alguns casos especificos, o objeto indicado necessitara de outro (alvo) para ser ativado (ex: usar chave porta).\n"
                        msgToSend += " >> Falar [texto]\n"
                        msgToSend += "     O jogador envia um texto que sera retransmitido para todos os jogadores presentes na sala atual.\n"
                        msgToSend += " >> Cochichar [texto] [jogador]\n"
                        msgToSend += "     O jogador envia uma mensagem de texto apenas para o jogador especificado, se ambos estiverem na mesma sala.\n"
                        msgToSend += " >> Ajuda\n"
                        msgToSend += "     Lista todos os comandos possiveis do jogo.\n"

                    self.sendMsg(msgToSend, endereco[0])   

                except:
                    self.sendMsg("404", endereco[0])   

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