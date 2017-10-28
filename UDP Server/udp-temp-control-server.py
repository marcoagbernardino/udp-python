import socket
import struct
import random

HOST = '' # all interfaces
UDP_PORT = 8802

#Protocolo da aplicação
TEMP_READING = (0x59)
LEDS_INDICATOR = (0x5A)
LEDS_STATE = (0x5B)
COOLER_PWM_DC = (0x5C)
PWM_STATE = (0x5D)

TEMP_FAIXA_MEDIA = (25)
TEMP_FAIXA_ALTA = (30)

ESCALA_LEDS_BAIXA = 4
ESCALA_LEDS_MEDIA = 2
ESCALA_LEDS_ALTA = 1

PWM_OFF = 1
PWM_V1 = 50
PWM_V2 = 90

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) # UDP IPv6
sock.bind((HOST, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    udp_client_addr = addr[0]
    upd_client_port = addr[1]
    offset = 0
    op, dados = struct.unpack_from("<Bi", data, offset)
    print op
    offset += struct.calcsize("<Bi")
    if op == TEMP_READING:
        temperatura = dados
        print "Leitura de temperatura do sensor [", udp_client_addr.strip(), "]:", upd_client_port, " -> ", temperatura
        #Enviar pacotes de LEDS_INDICATOR e COOLER_PWM_DC
        leds = 0
        pwm = 1
        if temperatura < TEMP_FAIXA_MEDIA:
            leds = ESCALA_LEDS_BAIXA
            pwm = PWM_OFF
        elif temperatura < TEMP_FAIXA_ALTA:
            leds = ESCALA_LEDS_MEDIA
            pwm = PWM_V1
        else:
            leds = ESCALA_LEDS_ALTA
            pwm = PWM_V2
        #envia a escala de leds
        data = struct.pack('<Bi', LEDS_INDICATOR, leds)
        sock.sendto(data, (udp_client_addr.strip(), UDP_PORT))
        
        #envia a velocidade do cooler
        data = struct.pack('<Bi', COOLER_PWM_DC, pwm)
        sock.sendto(data, (udp_client_addr.strip(), UDP_PORT))
    elif op == LEDS_STATE:
        leds = dados
        print "Status do indicador LED do sensor [", udp_client_addr.strip(), "]:", upd_client_port, " -> ", leds
    elif op == PWM_STATE:
        pwm = dados
        print "Velocidade do cooler do sensor [", udp_client_addr.strip(), "]:", upd_client_port, " -> ", pwm
    else:
        print "Operacao nao conhecida"
    