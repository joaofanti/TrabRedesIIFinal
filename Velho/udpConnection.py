import time
import socket
import netifaces as ni

class UDPConnection(object):  

    # Propriedades
    BuffSize = 2048         # Tamanho do buffer
    RespWait = 5            # Tempo de espera por uma resposta
    Buffer   = None         # Buffer que recebe a resposta
    Socket   = None         # Socket
    Nome     = None         # Nome da conexao
    Port     = 5005         # Porta de comunicacao
    IP       = "0.0.0.0"    # IP da conexao
    ID       = None         # ID da conexao
    GameID   = 'game-'      # ID para as mensagens enviadas pelo jogo

    """
        Inicializa uma nova instancia de UDPConnection
    """
    def __init__(self, ip, porta, id):
        self.IP     = ip
        self.Port   = porta
        self.ID     = id

        # Abre o socket
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

    """
    	Envia mensagem para o destino no formato "<identificador do requisitante>|<acao requisitada>".
    """
    def sendMsg(self, msg, ipDest, esperaResposta = False):

        # Envia mensagem
        formattedMsg = self.GameID + self.ID + '|' + msg
        self.Socket.sendto(formattedMsg, (ipDest, self.Port))

        # Aguarda a mensagem de retorno ser recebida em ate 10 segundos
        if (esperaResposta):
            respostaChegou = False
            limite = time.time() + self.RespWait
            while time.time() < limite:

                # Recebe os dados do socket
                self.Buffer, ipOrigemResposta = self.Socket.recvfrom(self.BuffSize)

                # Remove o header da mensagem (20 bytes)
                self.Buffer = self.Buffer[20:len(self.Buffer)]

                # Se a mensagem comeca com 'game' entao eh uma das mensagens do jogo
                if (self.Buffer.startswith(self.GameID)):

                    # Pega o identificador da mensagem removendo GameID da mesma e entao fazendo split pelo pipe, para divdir o ID e a mensagem/acao
                    idOrigem = self.Buffer[len(self.GameID):].split('|')[0]

                    # Se o IP da mensagem for o mesmo IP do destino e o ID da mensagem for diferente do ID proprio, entao recebeu mensagem
                    if (ipOrigemResposta[0] == ipDest and idOrigem != self.ID):
                        respostaChegou = True
                        break
            if (not respostaChegou):
                raise Exception('Resposta para mensagem nao foi recebida')
