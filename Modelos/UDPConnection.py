import socket
import netifaces as ni
from struct import *

"""
    Define uma conexao UDP generica.
"""
class UDPConnection(object):

    """
        Inicializa uma nova instancia de UDPConnection
    """
    def __init__(self, mac, ip, port, interface):
        self.MAC        = mac
        self.IP         = ip
        self.Port       = port
        self.Interface  = interface
        self.GameID     = "game"

        # Abre o socket raw
        self.SocketRcv = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        self.SocketSnd = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

    # Retorna a mensagem no formato correto
    def createMsg(self, _id, msg):
        return '{}-{}|{}'.format(self.GameID, _id, msg)

    # Converte o endereco MAC
    def eth_addr(self, a) :
        b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
        return b

    """
        Monta o cabecalho Ethernet.
         0                   1                   2                   3
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |       Ethernet destination address (first 32 bits)            |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        | Ethernet dest (last 16 bits)  |Ethernet source (first 16 bits)|
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |       Ethernet source address (last 32 bits)                  |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |        Type code              |                               |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    """
    def buildEth(self, srcMac, dstMac):
        ethertype = 0x0800 # IPv4
        return pack("!6s6sH", str(dstMac), str(srcMac), ethertype)

    """
        Monta o cabecalho IP.
         0                   1                   2                   3
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |Version|  IHL  |Type of Service|          Total Length         |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |         Identification        |Flags|      Fragment Offset    |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |  Time to Live |    Protocol   |         Header Checksum       |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                       Source Address                          |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                    Destination Address                        |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                    Options                    |    Padding    |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    """
    def buildIp(self, srcIp, dstIp, udpLength):

        # Configuracao basica do IP
        ip_ver = 4
        ip_ihl = 5
        ip_tos = 0
        ip_tot_len = 20 + udpLength # 32 bits do IPv4 mais o tamanho dos dados do UDP
        ip_id = 54321
        ip_frag_off = 0
        ip_ttl = 255
        ip_proto = socket.IPPROTO_UDP   # Protocolo seguinte: UDP.
        ip_check = 0                    # O proprio kernel vai inserir o checksum correto.
        ip_saddr = socket.inet_aton(srcIp)
        ip_daddr = socket.inet_aton(dstIp)

        ip_ihl_ver = (ip_ver << 4) + ip_ihl

        # Empacota num header
        ip_header = pack('!BBHHHBBH4s4s' , ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)  
        return ip_header

    """
        Monta o cabecalho UDP.
        0                   1                   2                   3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |          Source Port          |       Destination Port        |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |            Length             |           Checksum            |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                       .... data ....                          |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    """
    def buildUdp(self, srcPort, dstPort, msgLength):
        checksum = 0xffff # Nao utilizaremos checksum
        udp_header = pack('!HHHH' , srcPort, dstPort, msgLength + 8, checksum)
        return udp_header

    """
        Constroi o pacote completo Ethernet-IPv4-UDP com as informacoes fornecidas.
    """
    def buildFullPack(self, dstMac, dstIp, dstPort, msg):

        # Monta header UDP
        udpHeader = self.buildUdp(self.Port, dstPort, len(msg))

        # Monta header IPv4
        ipHeader = self.buildIp(self.IP, dstIp, len(udpHeader) + len(msg))

        # Monta header Ethernet
        ethHeader = self.buildEth(self.MAC, dstMac)

        # Junta os pacotes num so
        pct = ethHeader + ipHeader + udpHeader + msg
        return pct

    """
    	Envia mensagem para o destino.
    """
    def sendMsg(self, dstMac, dstIp, dstPort, msg):
        # Envia o pacote ao IP destino.
        pct = self.buildFullPack(dstMac, dstIp, dstPort, msg)
        return self.SocketSnd.sendto(pct, (self.Interface, 0))

    """
        Le mensagem do socket (descompacta cada campo e valida se eh uma mensagem do jogo, se for, retorna a mensagem).
    """
    def readMsg(self):

        # Recebe a mensagem
        packet = self.SocketRcv.recvfrom(2048)
        packet = packet[0]

        # Faz o parse do Ethernet
        eth_length = 14
        eth_header = packet[:eth_length]
        eth = unpack('!6s6sH' , eth_header)
        eth_protocol = socket.ntohs(eth[2])

        SOURCE_mac = self.eth_addr(packet[6:12])
 
        # Se for IPv4, faz o parse.
        if eth_protocol == 8 :

            # Pega os 20 primeiros chars do IP header
            ip_header = packet[eth_length:20+eth_length]
             
            # Unpack
            iph = unpack('!BBHHHBBH4s4s' , ip_header)
     
            version_ihl = iph[0]
            ihl = version_ihl & 0xF
     
            iph_length = ihl * 4
     
            protocol = iph[6]
            SOURCE_addr = socket.inet_ntoa(iph[8]);
            d_addr = socket.inet_ntoa(iph[9]);

            if (d_addr == self.IP):

                # Se for UDP, faz o parse.
                if protocol == 17 :
                    u = iph_length + eth_length
                    udph_length = 8
                    udp_header = packet[u:u+8]
         
                    # Dsempacota
                    udph = unpack('!HHHH' , udp_header)

                    SOURCE_port = udph[0]
                    dest_port = udph[1]
                    if (dest_port == self.Port):

                        # Pega os dados do pacote e verifica se inicia com o GameID
                        h_size = eth_length + iph_length + udph_length
                        data = packet[h_size:]
                        if (data.startswith(self.GameID)):
                            ans = {
                                "source_mac": SOURCE_mac,
                                "source_ip": SOURCE_addr,
                                "source_port": SOURCE_port,
                                "message": data
                            }
                            return ans

        return None
