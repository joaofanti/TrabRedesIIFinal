import socket

class Cliente:  

    # Propriedades do MUD CLIENT
    _UDP_IP = "0.0.0.0"         # IP do cliente
    _UDP_PORT = 5006            # Porta do cliente
    _Socket = None              # Socket UDP para comunicacao com o servidor
    _Tamanho_Do_Buffer = 1024   # Tamanho dos dados recebidos no socket
    _Nome = ""                  # Nome do jogador
    _ServerIP = "0.0.0.0"       # Nome do jogador
    _Buffer = ""                # Buffer de resposta do servidor

    """
        Inicializa uma nova instancia de MUD CLIENT
    """
    def __init__(self, ip, port, nome, serverIp):
        self._UDP_IP = ip
        self._UDP_PORT = port
        self._Socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        self._Socket.bind((self._UDP_IP, self._UDP_PORT))
        self._Tamanho_Do_Buffer = 1024
        self._Nome = nome
        self._ServerIP = serverIp

    """
    	Envia mensagem para o servidor no formato '<nome>|<comando>' e aguarda ate receber uma mensagem de resposta do servidor.
    	Entao, salva no buffer para ser analizada depois.
    """
    def enviaMensagem(self, mensagem):
        mensagem = self._Nome + '|' + mensagem
        self._Socket.sendto(mensagem, (self._ServerIP, self._UDP_PORT))
        while True:
            self._Buffer, endereco = self._Socket.recvfrom(self._Tamanho_Do_Buffer)
            self._Buffer = self._Buffer[20:len(self._Buffer)] # Remove o header da mensagem
            if (endereco[0] == self._ServerIP):
                break

    """
        Le o buffer e notifica o usuario corretamente
    """
    def leResposta(self):
        if self._Buffer == "200": # OK
            print "Comando executado com sucesso."
        elif self._Buffer == "201": # Created
            print "Cliente conectado com sucesso."
        elif self._Buffer == "400": # Bad Request
            print "Comando falhou."
        else:
            print self._Buffer

# --------------------------------------------------

"""
    Metodo principal para rodar o cliente
"""
if __name__ == "__main__":

    # Tenta conectar o jogador no servidor ate conseguir a conexao
    nomeJogador = ""
    conectado = False
    cliente = None

    while not conectado:
        nomeJogador = raw_input("Insira o nome do jogador: ")
        ipServidor = raw_input("Insira o endereco IP do servidor: ")

        # Pega o IP do cliente pela propria maquina. Entretanto, se estiver rodando tanto o servidor como o cliente na mesma maquina,
        # transforma o ip do cliente para localhost para poder testar
        ipCliente = socket.gethostbyname(socket.gethostname())
        if (ipCliente == ipServidor):
            ipCliente = "localhost"
        
        cliente = Cliente(ipCliente, 5006, nomeJogador, ipServidor)
        cliente.enviaMensagem("CriaConexao")
        cliente.leResposta()
        if (cliente._Buffer == "201"):
            conectado = True

    print "\n-----------------------------\n"
    print "Ola, " + nomeJogador
    print "Para jogar, digite um comando e pressione [ENTER]."
    print "Nota: digite o comando 'Ajuda' para obter a lista de todos os comandos do jogo."

    while True:
        cmd = raw_input("[CMD]: ")
        cliente.enviaMensagem(cmd)
        cliente.leResposta()