from UDPConnection import UDPConnection
import netifaces
import socket

from threading import Thread

"""
    Metodo principal para rodar o cliente
"""
if __name__ == "__main__": 
	ip = "192.168.0.14"
	port = 5006
	interface = "wlp6s0"
	mac = "14:2d:27:e2:83:8f"#netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]["addr"]
	udpConn = UDPConnection(mac, ip, port, interface)
	udpConn.sendMsg(mac, ip, 5005, "game-Bruno|CriaConexao")



	