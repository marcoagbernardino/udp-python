import socket
import struct
import random

#server:
UDP_PORT = 8802
UDP_IP = "2804:7f4:3b80:9440:5748:f6e0:f733:4c6b"


#Protocolo:
LED_TOGGLE_REQUEST = (0x79)
LED_SET_STATE = (0x7A)
LED_GET_STATE = (0x7B)
LED_STATE = (0x7C)

print "UDP server IP: ", UDP_IP
print "UDP server port: ", UDP_PORT

# socket.SOCK_DGRAM = UPD connection
led = 0 #valor inicial dos "leds"

print "Enviando LED_TOGGLE_REQUEST para ", UDP_IP
data = struct.pack('>B', LED_TOGGLE_REQUEST)
sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
sock.sendto(data, (UDP_IP, UDP_PORT))

print "Aguardando resposta..."
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    offset = 0
    op, led = struct.unpack_from(">BB", data, offset)
    print "op: ", op, ", led: ", led
    offset += struct.calcsize(">BB")        
    if op == LED_SET_STATE:
        print "LED_SET_STATE recebido = ", led
        print "Enviando LED_STATE = ", led
        data = struct.pack('>BB', LED_STATE, led)
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        sock.sendto(data, (UDP_IP, UDP_PORT))
    break