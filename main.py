import RPi.GPIO as GPIO
import serial
import struct
from crc import calcula_CRC
import codecs
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

    if resultado_crc ==  resultado_crc_mensagem:
        return dado
    else:
        return False

# matricula = '\x08\x03\x02\x04'

# temp_interna = f'\x01\x23\xc1{matricula}'.encode('ascii')

# temp_interna = str.encode(temp_interna)


temp_interna = b'\x01\x23\xc1\x08\x03\x02\x04'

crc_tmp_interna = calcula_CRC(temp_interna, 7).to_bytes(2,'little')

uart.write(temp_interna + crc_tmp_interna)

recebe_uart = verifica_crc()

dados = struct.unpack("f",recebe_uart[3:-2])

print(dados[0])