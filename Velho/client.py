from socket import *
import struct


s = socket(AF_INET, SOCK_RAW, IPPROTO_UDP); # Abrindo o socket
data = 'JOAO :)'; # Data enviada pelo socket
sport = 4711;    # Porta de origem arbitraria
dport = 45134;   # Porte de destino arbitraria
length = 8+len(data);
checksum = 27199; # Tem que ser alterado, pode assumir valor 0 (no checksum) ou deve calcular o valor correto

udp_header = struct.pack('!HHHH', sport, dport, length, checksum);  #---> https://docs.python.org/3/library/struct.html#struct.pack 

s.sendto(udp_header+data, ('', 0)); # Enviando Pacote
