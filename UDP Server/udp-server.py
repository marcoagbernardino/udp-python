import socket
import struct
import random

HOST = '' # all interfaces
UDP_PORT = 8802

#Protocolo
LED_TOGGLE_REQUEST = (0x79)
LED_SET_STATE = (0x7A)
LED_GET_STATE = (0x7B)
LED_STATE = (0x7C)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP IPv4
sock.bind((HOST, UDP_PORT))


while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    udp_client_addr = addr[0]
    upd_client_port = addr[1]
    offset = 0
    op = struct.unpack_from(">B", data, offset)
    print op
    offset += struct.calcsize(">B")
    if op == LED_STATE:
        print "LED_STATE recebido de: [", udp_client_addr.strip(), "]:", upd_client_port
        led = struct.unpack_from(">Bi", data, offset)
        print "Valor: ", led
    if op == LED_TOGGLE_REQUEST:
        print "LED_TOGGLE_REQUEST recebido de: [", udp_client_addr.strip(), "]:", upd_client_port
        # responder ao cliente com um valor para acender os leds. LED_SET_STATE
    else:
        print "Operacao nao conhecida"