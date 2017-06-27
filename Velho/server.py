import socket

"""
    Representa um servidor MUD.
"""
class MudServer:

    # Propriedades do MUD SERVER
    _UDP_IP = "0.0.0.0"         # IP do servidor
    _UDP_PORT = 5005            # Porta do servidor
    _Socket = None              # Socket UDP para comunicacao com os clientes
    _Tamanho_Do_Buffer = 1024   # Tamanho dos dados recebidos no socket
    _Clientes_Conectados = {}   # Dicionario de clientes conectados

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
    def __init__(self, ip, port):
        self._UDP_IP = ip
        self._UDP_PORT = port
        self._Socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        self._Socket.bind((self._UDP_IP, self._UDP_PORT))
        self._Tamanho_Do_Buffer = 1024
        self._Clientes_Conectados = {}

    """
        Escuta os dados recebidos pelo socket e executa a logica num laco infinito
    """
    def atualiza(self):
        # Recebe os dados pelo socket
        mensagem, endereco = self._Socket.recvfrom(self._Tamanho_Do_Buffer)

        # Remove o header da mensagem
        mensagem = mensagem[20:len(mensagem)]

        # Particiona a mensagem, separando por espacos e buscando o nome do jogador que requisitou o comando
        mensagemSplit = mensagem.split('|')
        nomeJogador = mensagemSplit[0]

        if (len(mensagemSplit) == 2):
            mensagemSplit = mensagemSplit[1].split(' ')

        mensagemParaEnviar = None

        # Verifica se foi um novo pedido de conexao e realiza nova conexao se necessario
        if (mensagemSplit[0] == self._CMD_NOVA_CONEXAO):
            if (nomeJogador in self._Clientes_Conectados):
                mensagemParaEnviar = "400"
            else:
                self._Clientes_Conectados[nomeJogador] = endereco[0]
                mensagemParaEnviar ="201"
                print "Novo jogador conectado: ", nomeJogador, " (", endereco[0], ")"

        # Se nao, verifica se jogador ja esta conectado e, caso esteja, verifica qual comando foi solicitado
        elif (nomeJogador in self._Clientes_Conectados):
            
            print '[', nomeJogador, '] solicitiou o comando "', mensagemSplit[0], '"'
            
            mensagemParaEnviar = "400"

            # Ajuda
            if (mensagemSplit[0] == self._CMD_AJUDA):
                mensagemParaEnviar += "Examinar [sala/objeto]\n"
                mensagemParaEnviar += "     Retorna a descricao da sala atual (sala) ou objeto mencionado.\n"
                mensagemParaEnviar += "     A descricao da sala tambem deve listar as salas adjacentes e suas respectivas direcoes, objetos e demais jogadores presentes no local.\n"
                mensagemParaEnviar += "Mover [N/S/L/O]\n"
                mensagemParaEnviar += "     O jogador deve mover-se para a direcao indicada (norte, sul, leste ou oeste).\n"
                mensagemParaEnviar += "     Ao entrar numa nova sala, o jogo deve executar automaticamente o comando 'examinar sala', que descreve o novo ambiente ao jogador.\n"
                mensagemParaEnviar += "Pegar [objeto]\n"
                mensagemParaEnviar += "     O jogador coleta um objeto que esta na sala atual.\n"
                mensagemParaEnviar += "     Alguns objetos nao podem ser coletados, como no caso de 'porta'.\n"
                mensagemParaEnviar += "Largar [objeto]\n"
                mensagemParaEnviar += "     O jogador larga um objeto que esta no seu inventorio, na sala atual.\n"
                mensagemParaEnviar += "Inventorio\n"
                mensagemParaEnviar += "     O jogo lista todos os objetos carregados atualmente pelo jogador.\n"
                mensagemParaEnviar += "Usar [objeto] {alvo}\n"
                mensagemParaEnviar += "     O jogador usa o objeto mencionado;\n"
                mensagemParaEnviar += "     Em alguns casos especificos, o objeto indicado necessitara de outro (alvo) para ser ativado (ex: usar chave porta).\n"
                mensagemParaEnviar += "Falar [texto]\n"
                mensagemParaEnviar += "     O jogador envia um texto que sera retransmitido para todos os jogadores presentes na sala atual.\n"
                mensagemParaEnviar += "Cochichar [texto] [jogador]\n"
                mensagemParaEnviar += "     O jogador envia uma mensagem de texto apenas para o jogador especificado, se ambos estiverem na mesma sala.\n"
                mensagemParaEnviar += "Ajuda\n"
                mensagemParaEnviar += "     Lista todos os comandos possiveis do jogo.\n"

        if (mensagemParaEnviar != None):
            self._Socket.sendto(mensagemParaEnviar, endereco)

# --------------------------------------------------

"""
    Metodo principal para rodar o servidor
"""
if __name__ == "__main__":
    servidor = MudServer(socket.gethostbyname(socket.gethostname()), 5005)
    print "Servidor MUD inicializado com sucesso em ", servidor._UDP_IP, " [", servidor._UDP_PORT, "] "
    while True:
        servidor.atualiza()