import RPi.GPIO as GPIO
import serial
import struct
from crc import calcula_CRC
import codecs
import time

ventoinha = 24
resistor = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ventoinha, GPIO.OUT)
GPIO.setup(resistor, GPIO.OUT)


uart = serial.Serial("/dev/serial0")

def verifica_crc(tamanho_leitura = 9, tamanho_crc = 7):
    dado = uart.read(tamanho_leitura)
    
    resultado_crc = calcula_CRC(dado[:-2],tamanho_crc).to_bytes(2,'little')
    resultado_crc_mensagem = dado[-2:]

    print(resultado_crc)
    print(resultado_crc_mensagem)
    if resultado_crc ==  resultado_crc_mensagem:
        return dado
    else:
        return verifica_crc()

# matricula = '\x08\x03\x02\x04'

# temp_interna = b'\x01\x23\xc1'+ matricula

# temp_interna = str.encode(temp_interna)


# ----------------------------- TEMPERATURA INTERNA-------------------------------------------------
temp_interna = b'\x01\x23\xc1\x08\x03\x02\x04'

crc_tmp_interna = calcula_CRC(temp_interna, 7).to_bytes(2,'little')

uart.write(temp_interna + crc_tmp_interna)

recebe_uart = verifica_crc()

dados = struct.unpack("f",recebe_uart[3:-2])

print(dados[0])

# ----------------------------- TEMPERATURA REFERENCIAL -------------------------------------------------
temp_referencial = b'\x01\x23\xc2\x08\x03\x02\x04'

crc_tmp_referencial = calcula_CRC(temp_referencial, 7).to_bytes(2,'little')

uart.write(temp_referencial + crc_tmp_referencial)

recebe_uart = verifica_crc()

temp_referencial = struct.unpack("f",recebe_uart[3:-2])

print(temp_referencial[0])


# ----------------------------- LÊ COMANDOS DO USUÁRIO  -------------------------------------------------

# aux = b'\x00#\xc3\x00\x00\x00\x00CB'
# while True:
#     usuario = b'\x01\x23\xc3\x08\x03\x02\x04'

#     crc_usuario = calcula_CRC(usuario, 7).to_bytes(2,'little')

#     uart.write(usuario + crc_usuario)

   
#     recebe_uart = verifica_crc()

#     # print(recebe_uart)
#     if '0x0' != str(hex(recebe_uart[3])):

#         print(str(hex(recebe_uart[3])))

#         if str(hex(recebe_uart[3])) == '0xa1':
#             liga_forno = b'\x01\x16\xd3\x08\x03\x02\x04\x01'

#             liga_forno_crc = calcula_CRC(liga_forno, 8).to_bytes(2,'little')
#             uart.write(liga_forno + liga_forno_crc)

#             recebe_forno = verifica_crc()

#         if str(hex(recebe_uart[3])) == '0xa2':
#             desliga_forno = b'\x01\x16\xd3\x08\x03\x02\x04\x00'

#             desliga_forno_crc = calcula_CRC(desliga_forno, 8).to_bytes(2,'little')
#             uart.write(desliga_forno + desliga_forno_crc)

#             recebe_forno = verifica_crc()

#             print(recebe_forno)
        
#         if str(hex(recebe_uart[3])) == '0xa3':
#             inicia_aquecimento = b'\x01\x16\xd5\x08\x03\x02\x04\x01'

#             inicia_aquecimento_crc = calcula_CRC(inicia_aquecimento, 8).to_bytes(2,'little')
#             uart.write(inicia_aquecimento + inicia_aquecimento_crc)

#             recebe_forno = verifica_crc()

#             print(recebe_forno)

#         if str(hex(recebe_uart[3])) == '0xa4':
#             desliga_aquecimento = b'\x01\x16\xd5\x08\x03\x02\x04\x00'

#             desliga_aquecimento_crc = calcula_CRC(desliga_aquecimento, 8).to_bytes(2,'little')
#             uart.write(desliga_aquecimento + desliga_aquecimento_crc)

#             recebe_forno = verifica_crc()

#             print(recebe_forno)

#         if str(hex(recebe_uart[3])) == '0xa5':
#             curva = b'\x01\x16\xd4\x08\x03\x02\x04\x00'

#             curva_crc = calcula_CRC(curva, 8).to_bytes(2,'little')
#             uart.write(curva + curva_crc)

#             recebe_forno = verifica_crc()

#             print(recebe_forno)

#     else:
#         time.sleep(0.5)
#         aux = recebe_uart
#         continue



#----------------------------- ENVIA SINAL DE CONTROLE  -------------------------------------------------

# hex(random(range(0,100)))
teste = 20
teste = teste.to_bytes(4,'little')
sinal_controle = b'\x01\x16\xd1\x08\x03\x02\x04' + teste

sinal_controle_crc = calcula_CRC(sinal_controle, len(sinal_controle)).to_bytes(2,'little')

print(sinal_controle + sinal_controle_crc)

uart.write(sinal_controle + sinal_controle_crc)

recebe_uart = verifica_crc(5,3)

# sinal_controle = struct.unpack("f",recebe_uart[:-2])

# print(sinal_controle[0])

print(recebe_uart)