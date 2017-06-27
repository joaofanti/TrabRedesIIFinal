import socket

"""
    Representa um servidor MUD.
"""
class MudServer:

    """
        Representa um cliente conectado ao servidor
    """
    class _Cliente:
        endereco = ""   # Endereco do cliente conectado
        buffer = ""     # Mensagem recebida pelo cliente

    _UDP_IP = "0.0.0.0"         # IP para abrir o socket
    _UDP_PORT = 5005            # Porta para abrir o socket
    _Socket = None              # Socket UDP para comunicacao com os clientes
    _Tamanho_Do_Buffer = 1024   # Tamanho dos dados recebidos no socket
    _Clientes_Conectados = {}   # Dicionario de clientes conectados

    # Lista de comandos
    _CMD_NOVA_CONEXAO = "NovaConexao"
    _CMD_EXAMINAR = "Examinar"
    # TODO: adicionar novos comandos

    def __init__(self, ip, port):
        self._UDP_IP = ip
        self._UDP_PORT = port
        self._Socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        self._Socket.bind((self._UDP_IP, self._UDP_PORT))
        self._Tamanho_Do_Buffer = 1024
        self._Clientes_Conectados = {}

    # Adiciona um novo cliente a lista de clientes conectados
    def novaConexao(self, nome, endereco):
        self._Clientes_Conectados[nome] = endereco
        print "Novo cliente conectado: ", nome

    # Escuta os dados recebidos pelo socket e executa a logica num laco infinito
    def atualiza(self):
        dados, endereco = self._Socket.recvfrom(self._Tamanho_Do_Buffer)
        dados = dados[20:len(dados)] # Remove o header da mensagem

        # Verifica cada comando
        if (str.startswith(dados, _CMD_NOVA_CONEXAO)):
            tamanhoDoComando = len(self._CMD_NOVA_CONEXAO) + 1
            nome = dados[tamanhoDoComando:len(dados)]
            # Se o endereco nao esta na lista ainda, adiciona como novo cliente (se for uma requisicao de novo cliente)
            if (nome not in self._Clientes_Conectados):
                endereco = endereco[0]
                self.novaConexao(nome, endereco)
                self._Socket.sendto("201", (endereco, self._UDP_PORT))
            else:

# --------------------------------------------------

# Metodo principal para rodar o servidor
if __name__ == "__main__":
    ipDoServidor = raw_input("Insira o endereco IP do SERVIDOR: ")
    portaDoServidor = input("Insira a porta do SERVIDOR: ")

    servidor = MudServer(ipDoServidor, portaDoServidor)

    print "Servidor MUD inicializado com sucesso."

    while True:
        servidor.atualiza()