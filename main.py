import RPi.GPIO as GPIO
import serial
import struct
from crc import calcula_CRC
import codecs
import time
from pid import pid_controle
import threading

ventoinha = 24
resistor = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ventoinha, GPIO.OUT)
GPIO.setup(resistor, GPIO.OUT)

ventoinha_pwm = GPIO.PWM(ventoinha,60)
resistor_pwm = GPIO.PWM(resistor,60)


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

# ------------------------------------------- GERA LOG --------------------------------------------
# temp_interna_binario = b'\x01\x23\xc1\x08\x03\x02\x04'
# crc_tmp_interna = calcula_CRC(temp_interna_binario, 7).to_bytes(2,'little')

# temp_referencial_binario = b'\x01\x23\xc2\x08\x03\x02\x04'
# crc_tmp_referencial = calcula_CRC(temp_referencial_binario, 7).to_bytes(2,'little')

# def gera_logs():
#     while True:
#         uart.write(temp_interna_binario + crc_tmp_interna)
#         recebe_uart = verifica_crc()
#         temp_interna = struct.unpack("f",recebe_uart[3:-2])
#         temp_interna = temp_interna[0]

#         uart.write(temp_referencial_binario + crc_tmp_referencial)
#         recebe_uart = verifica_crc()
#         temp_referencial = struct.unpack("f",recebe_uart[3:-2])
#         temp_referencial = temp_referencial[0]






# ----------------------------- TEMPERATURA INTERNA-------------------------------------------------

# temp_interna = b'\x01\x23\xc1\x08\x03\x02\x04'

# crc_tmp_interna = calcula_CRC(temp_interna, 7).to_bytes(2,'little')

# uart.write(temp_interna + crc_tmp_interna)

# recebe_uart = verifica_crc()

# temp_interna = struct.unpack("f",recebe_uart[3:-2])

# print(temp_interna[0])

# ----------------------------- TEMPERATURA REFERENCIAL -------------------------------------------------

# temp_referencial = b'\x01\x23\xc2\x08\x03\x02\x04'

# crc_tmp_referencial = calcula_CRC(temp_referencial, 7).to_bytes(2,'little')

# uart.write(temp_referencial + crc_tmp_referencial)

# recebe_uart = verifica_crc()

# temp_referencial = struct.unpack("f",recebe_uart[3:-2])

# print(temp_referencial[0])

# ----------------------------- LÊ COMANDOS DO USUÁRIO  -------------------------------------------------

aux = b'\x00#\xc3\x00\x00\x00\x00CB'
inicia = False

while True:

    # TEMPERATURA INTERNA
    temp_interna = b'\x01\x23\xc1\x08\x03\x02\x04'
    crc_tmp_interna = calcula_CRC(temp_interna, 7).to_bytes(2,'little')
    uart.write(temp_interna + crc_tmp_interna)
    recebe_uart = verifica_crc()
    temp_interna = struct.unpack("f",recebe_uart[3:-2])
    #print(temp_interna[0])

    # TEMPERATURA REFERENCIAL
    temp_referencial = b'\x01\x23\xc2\x08\x03\x02\x04'
    crc_tmp_referencial = calcula_CRC(temp_referencial, 7).to_bytes(2,'little')
    uart.write(temp_referencial + crc_tmp_referencial)
    recebe_uart = verifica_crc()
    temp_referencial = struct.unpack("f",recebe_uart[3:-2])
    #print(temp_referencial[0])


    # CALCULA PID E PWM

    if inicia:
        valor_pid = pid_controle(temp_interna[0],referencia = temp_referencial[0])
        if valor_pid < 0:
            ventoinha_pwm.start(valor_pid * -1)
            resistor_pwm.stop()
        else:
            resistor_pwm.start(valor_pid)
            ventoinha_pwm.stop()

        valor_pid_binario = int(valor_pid).to_bytes(4,'little',signed = True)
        sinal_controle = b'\x01\x16\xd1\x08\x03\x02\x04' + valor_pid_binario
        sinal_controle_crc = calcula_CRC(sinal_controle, len(sinal_controle)).to_bytes(2,'little')
        #print(sinal_controle + sinal_controle_crc)
        uart.write(sinal_controle + sinal_controle_crc)
        # recebe_uart = verifica_crc(5,3)


    # LE COMANDOS DO USUARIO
    le_usuario = b'\x01\x23\xc3\x08\x03\x02\x04'
    crc_le_usuario = calcula_CRC(le_usuario, 7).to_bytes(2,'little')
    uart.write(le_usuario + crc_le_usuario)
    recebe_uart = verifica_crc()

    # print(recebe_uart)
    if '0x0' != str(hex(recebe_uart[3])):

        print(str(hex(recebe_uart[3])))

        if str(hex(recebe_uart[3])) == '0xa1':

            print('LIGOU FORNO')
            liga_forno = b'\x01\x16\xd3\x08\x03\x02\x04\x01'

            liga_forno_crc = calcula_CRC(liga_forno, 8).to_bytes(2,'little')
            uart.write(liga_forno + liga_forno_crc)

            recebe_forno = verifica_crc()

        if str(hex(recebe_uart[3])) == '0xa2':
            print('DESLIGA FORNO')
            desliga_forno = b'\x01\x16\xd3\x08\x03\x02\x04\x00'

            desliga_forno_crc = calcula_CRC(desliga_forno, 8).to_bytes(2,'little')
            uart.write(desliga_forno + desliga_forno_crc)

            recebe_forno = verifica_crc()

            #print(recebe_forno)
        
        if str(hex(recebe_uart[3])) == '0xa3':
            print('INICIA AQUECIMENTO')
            inicia = True
            inicia_aquecimento = b'\x01\x16\xd5\x08\x03\x02\x04\x01'

            inicia_aquecimento_crc = calcula_CRC(inicia_aquecimento, 8).to_bytes(2,'little')
            uart.write(inicia_aquecimento + inicia_aquecimento_crc)

            recebe_forno = verifica_crc()

            #print(recebe_forno)

        if str(hex(recebe_uart[3])) == '0xa4':
            print('DESLIGA AQUECIMENTO')
            inicia = False
            desliga_aquecimento = b'\x01\x16\xd5\x08\x03\x02\x04\x00'

            desliga_aquecimento_crc = calcula_CRC(desliga_aquecimento, 8).to_bytes(2,'little')
            uart.write(desliga_aquecimento + desliga_aquecimento_crc)

            recebe_forno = verifica_crc()

            print(recebe_forno)

        if str(hex(recebe_uart[3])) == '0xa5':
            print('MODO CURVA')
            curva = b'\x01\x16\xd4\x08\x03\x02\x04\x00'

            curva_crc = calcula_CRC(curva, 8).to_bytes(2,'little')
            uart.write(curva + curva_crc)



            recebe_forno = verifica_crc()

            print(recebe_forno)

        
    else:
        time.sleep(0.5)
        aux = recebe_uart
        continue
    
    time.sleep(2)



#----------------------------- ENVIA SINAL DE CONTROLE  -------------------------------------------------



# valor_pid = pid_controle(temp_interna[0],referencia = temp_referencial[0])

# if valor_pid < 0:
#     ventoinha_pwm.start(valor_pid)
#     resistor_pwm.stop()
# else:
#     resistor_pwm.start(valor_pid)
#     ventoinha_pwm.stop()



# valor_pid_binario = int(valor_pid).to_bytes(4,'little',signed = True)

# sinal_controle = b'\x01\x16\xd1\x08\x03\x02\x04' + valor_pid_binario



# sinal_controle_crc = calcula_CRC(sinal_controle, len(sinal_controle)).to_bytes(2,'little')

# print(sinal_controle + sinal_controle_crc)

# uart.write(sinal_controle + sinal_controle_crc)

# recebe_uart = verifica_crc(5,3)

# # sinal_controle = struct.unpack("f",recebe_uart[:-2])

# # print(sinal_controle[0])

# print(recebe_uart)