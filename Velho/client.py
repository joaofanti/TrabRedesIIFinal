import socket

class Cliente:
    _UDP_IP = "0.0.0.0"         # IP do servidor
    _UDP_PORT = 5005            # Porta de comunicacao com o servidor
    _Socket = None     			# Socket UDP para comunicacao com os clientes
    _Nome = ""					# Nome do cliente
    _Tamanho_Do_Buffer = 1024	# Tamanho dos dados recebidos no socket
    _Buffer = None				# Buffer recebido pelo socket

    def __init__(self, ipClient, portClient, ipServer, portServer, nome):
    	self._UDP_IP = ipServer
        self._UDP_PORT = portServer
        self._Nome = nome
        self._Tamanho_Do_Buffer = 1024
        # Cria um socket raw com o protocolo UDP
        self._Socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        self._Socket.bind((ipClient, portClient))
        self.enviaMensagem("NovaConexao " + self._Nome)
        
        # Se a resposta nao for 201 (codigo HTTP "Created") entao a operacao falhou
        print self._Buffer
        if (self._Buffer != "201"):
        	raise Exception('Cliente nao conseguiu conectar-se ao servidor.')

    """
    	Envia mensagem para o servidor e aguarda ate receber uma mensagem de resposta do servidor.
    	Entao, salva no buffer para ser analizada depois.
    """
    def enviaMensagem(self, mensagem):
        self._Socket.sendto(mensagem, (self._UDP_IP, self._UDP_PORT))
        while True:
            self._Buffer, endereco = self._Socket.recvfrom(self._Tamanho_Do_Buffer)
            self._Buffer = self._Buffer[20:len(self._Buffer)] # Remove o header da mensagem
            if (endereco[0] == self._UDP_IP):
                break

    def leResposta(self):
        if self._Buffer == "200": # OK
            print "Comando executado com sucesso."
        elif self._Buffer == "201": # Created
            print "Cliente conectado com sucesso."
        elif self._Buffer == "400": # Bad Request
            print "Comando falhou."
        else:
            print "O servidor nao identificou o comando digitado."

# --------------------------------------------------

# Metodo principal para rodar o cliente
if __name__ == "__main__":
    ipDoCliente = raw_input("Insira o endereco IP do CLIENTE: ")
    portaDoCliente = input("Insira a porta do CLIENTE: ")

    ipDoServidor = raw_input("Insira o endereco IP do SERVIDOR: ")
    portaDoServidor = input("Insira a porta do SERVIDOR: ")

    nomeDoJogador = raw_input("Insira o nome do jogador: ")

    cliente = Cliente(ipDoCliente, portaDoCliente, ipDoServidor, portaDoServidor, nomeDoJogador)
    cliente.leResposta()

    print "Ola, " + nomeDoJogador + "!"
    print "Para jogar, digite um comando e pressione [ENTER]."
    print "Nota: digite o comando 'Ajuda' para obter a lista de todos os comandos do jogo."

    while True:
        cmd = raw_input("[CMD]: ")
        cliente.enviaMensagem(cmd)
        cliente.leResposta()
