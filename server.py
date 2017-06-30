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
        Inicializa uma nova instancia de MUD SERVER
    """
    def __init__(self, ip, porta):
        self.ConnectedClients = {}
        UDPConnection.__init__(self, ip, porta, 'server')

        # Le o texto para resposta do comando 'Ajuda'
        f = open('Recursos/Ajuda.txt', 'r') 
        self.TextoAjuda = f.read() 

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
                        msgToSend = self.TextoAjuda
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
