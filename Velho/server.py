from socket import *
import struct


s = socket(AF_INET, SOCK_RAW, IPPROTO_UDP); # Abrindo o socket

while(True):
	response, addr = s.recvfrom(4711);
	print len(response)
	response_id = struct.unpack('!HHHHHHHHHHHHHHHHHH', response);
	print response_id
