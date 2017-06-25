#import socket, select, time
#s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s1.bind(('192.168.0.28', 45134))
#s1 = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
#s1.bind(('192.168.0.28', 45134))
#while True:
#    r, w, x = select.select([s1], [], [])
#    time.sleep(1)
#    for i in r:
#    	print "\n"
#        print i, i.recvfrom(131072)


import socket

UDP_IP = "192.168.0.28"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
sock.bind((UDP_IP, UDP_PORT))

while True:
	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	if(len(data) < 50):
		print "\nReceived message:", data
		print "\nTamanho: ", len(data)