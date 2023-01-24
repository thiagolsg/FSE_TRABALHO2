import RPi.GPIO as GPIO
import serial
import struct
from crc import calcula_CRC
import time
from pid import pid_controle
from i2c import temperatura_ambiente
import csv
from datetime import datetime
from config import solicita_temperatura_interna,solicita_temperatura_referencial,le_usuario,liga_forno,desliga_forno,inicia_aquecimento,desliga_aquecimento,liga_curva,desliga_curva

# CONFIGURAÇÕES DA GPIO
ventoinha = 24
resistor = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ventoinha, GPIO.OUT)
GPIO.setup(resistor, GPIO.OUT)

ventoinha_pwm = GPIO.PWM(ventoinha,60)
resistor_pwm = GPIO.PWM(resistor,60)

# Inicializando a UART
uart = serial.Serial("/dev/serial0")

# Verifica o crc de cada comando recebido da uart
def verifica_crc(tamanho_leitura = 9, tamanho_crc = 7):
    dado = uart.read(tamanho_leitura)

    resultado_crc = calcula_CRC(dado[:-2],tamanho_crc).to_bytes(2,'little')
    resultado_crc_mensagem = dado[-2:]

    if resultado_crc ==  resultado_crc_mensagem:
        return dado
    else:
        return verifica_crc()


# Valores globais
inicia = False
Kp = 30
Ki = 0.2
Kd = 400.0
forno_estado = False
modo_curva = False
temp_referencial = 0
temp_interna = 0
modo_terminal = False

# Desliga todo o sistema
uart.write(desliga_curva)
uart.write(desliga_aquecimento)
uart.write(desliga_forno)
resistor_pwm.stop()
ventoinha_pwm.stop()

entrada_temperatura = input('Deseja Alterar o valor da temperatura de referencia? S/N \n')

if entrada_temperatura != 'N':

   
    uart.write(liga_curva)
    recebe_uart = verifica_crc()
    
    modo_curva = True
    modo_terminal = True
    temperatura_usuario = float(input('Digite o Valor da temperatura \n'))
    temperatura_usuario_binario = struct.pack('f', temperatura_usuario)
    envia_temperatura = b'\x01\x16\xd2\x08\x03\x02\x04' + temperatura_usuario_binario
    crc_envia_temperatura = calcula_CRC(envia_temperatura, len(envia_temperatura)).to_bytes(2,'little')
    uart.write(envia_temperatura + crc_envia_temperatura)
    
    
entrada_pid = input('Deseja escolher os parametros do PID? S/N \n')

if entrada_pid != 'N':
    Kp = float(input('Digite o valor de Kp\n'))
    Ki = float(input('Digite o valor de Ki\n'))
    Kd = float(input('Digite o valor de Kd\n'))

print('Acompanhe pelo Dashboard\n')

# Contador da curva reflow
count = 0
try:
    while True:
        

        # TEMPERATURA INTERNA
        uart.flushInput() # Limpa o buffer
        uart.write(solicita_temperatura_interna)
        recebe_uart = verifica_crc()
        temp_interna = struct.unpack("f",recebe_uart[3:-2])

        # ENVIA TEMPERATURA
        if modo_terminal:
            uart.write(envia_temperatura + crc_envia_temperatura)

        # TEMPERATURA REFERENCIAL
        if modo_curva == False:
            uart.write(solicita_temperatura_referencial)
            recebe_uart = verifica_crc()
            temp_referencial = struct.unpack("f",recebe_uart[3:-2])

        elif modo_terminal == True:
            uart.write(solicita_temperatura_referencial)
            recebe_uart = verifica_crc()
            temp_referencial = struct.unpack("f",recebe_uart[3:-2])

        elif modo_terminal == False:
            if count >= 0 and count < 60:
                temp_referencial = [25]
                temperatura_reflow = struct.pack('f', 25)
                envia_temperatura = b'\x01\x16\xd2\x08\x03\x02\x04' + temperatura_reflow
                crc_envia_temperatura = calcula_CRC(envia_temperatura, len(envia_temperatura)).to_bytes(2,'little')
                uart.write(envia_temperatura + crc_envia_temperatura)
                    
            elif count >= 60 and count < 120:
                temp_referencial = [38]
                temperatura_reflow = struct.pack('f', 38)
                envia_temperatura = b'\x01\x16\xd2\x08\x03\x02\x04' + temperatura_reflow
                crc_envia_temperatura = calcula_CRC(envia_temperatura, len(envia_temperatura)).to_bytes(2,'little')
                uart.write(envia_temperatura + crc_envia_temperatura)

            elif count >= 120 and count < 240:
                temp_referencial = [46]
                temperatura_reflow = struct.pack('f', 46)
                envia_temperatura = b'\x01\x16\xd2\x08\x03\x02\x04' + temperatura_reflow
                crc_envia_temperatura = calcula_CRC(envia_temperatura, len(envia_temperatura)).to_bytes(2,'little')
                uart.write(envia_temperatura + crc_envia_temperatura)
                    
            elif count >= 240 and count < 260:
                temp_referencial = [54]
                temperatura_reflow = struct.pack('f', 54)
                envia_temperatura = b'\x01\x16\xd2\x08\x03\x02\x04' + temperatura_reflow
                crc_envia_temperatura = calcula_CRC(envia_temperatura, len(envia_temperatura)).to_bytes(2,'little')
                uart.write(envia_temperatura + crc_envia_temperatura)

            elif count >= 260 and count < 300:
                temp_referencial = [57]
                temperatura_reflow = struct.pack('f', 57)
                envia_temperatura = b'\x01\x16\xd2\x08\x03\x02\x04' + temperatura_reflow
                crc_envia_temperatura = calcula_CRC(envia_temperatura, len(envia_temperatura)).to_bytes(2,'little')
                uart.write(envia_temperatura + crc_envia_temperatura)

            elif count >= 300 and count < 360:
                temp_referencial = [61]
                temperatura_reflow = struct.pack('f', 61)
                envia_temperatura = b'\x01\x16\xd2\x08\x03\x02\x04' + temperatura_reflow
                crc_envia_temperatura = calcula_CRC(envia_temperatura, len(envia_temperatura)).to_bytes(2,'little')
                uart.write(envia_temperatura + crc_envia_temperatura)

            elif count >= 360 and count < 420:
                temp_referencial = [63]
                temperatura_reflow = struct.pack('f', 63)
                envia_temperatura = b'\x01\x16\xd2\x08\x03\x02\x04' + temperatura_reflow
                crc_envia_temperatura = calcula_CRC(envia_temperatura, len(envia_temperatura)).to_bytes(2,'little')
                uart.write(envia_temperatura + crc_envia_temperatura)

            elif count >= 420 and count < 480:
                temp_referencial = [54]
                temperatura_reflow = struct.pack('f', 54)
                envia_temperatura = b'\x01\x16\xd2\x08\x03\x02\x04' + temperatura_reflow
                crc_envia_temperatura = calcula_CRC(envia_temperatura, len(envia_temperatura)).to_bytes(2,'little')
                uart.write(envia_temperatura + crc_envia_temperatura)

            elif count >= 480 and count < 600:
                temp_referencial = [33]
                temperatura_reflow = struct.pack('f', 33)
                envia_temperatura = b'\x01\x16\xd2\x08\x03\x02\x04' + temperatura_reflow
                crc_envia_temperatura = calcula_CRC(envia_temperatura, len(envia_temperatura)).to_bytes(2,'little')
                uart.write(envia_temperatura + crc_envia_temperatura)

            elif count >= 600:
                temp_referencial = [25]
                temperatura_reflow = struct.pack('f', 25)
                envia_temperatura = b'\x01\x16\xd2\x08\x03\x02\x04' + temperatura_reflow
                crc_envia_temperatura = calcula_CRC(envia_temperatura, len(envia_temperatura)).to_bytes(2,'little')
                uart.write(envia_temperatura + crc_envia_temperatura)
            
            count += 1
           
        # ENVIA TEMPERATURA AMBIENTE
        temp_ambiente = temperatura_ambiente()
        temp_ambiente_binario = struct.pack('f', temp_ambiente)
        envia_ambiente = b'\x01\x16\xd6\x08\x03\x02\x04' + temp_ambiente_binario
        crc_envia_ambiente = calcula_CRC(envia_ambiente, len(envia_ambiente)).to_bytes(2,'little')
        uart.write(envia_ambiente + crc_envia_ambiente)

        # CALCULA PID E PWM
        valor_pid = 0
        if inicia:
            valor_pid = pid_controle(int(temp_interna[0]),referencia = temp_referencial[0],Kp=Kp,Ki=Ki,Kd=Kd)
            if valor_pid < 0:
                #Ligou ventoinha
                ventoinha_pwm.start(valor_pid * -1)
                resistor_pwm.stop()
            else:
                #Ligou resistor
                resistor_pwm.start(valor_pid)
                ventoinha_pwm.stop()

            valor_pid_binario = int(valor_pid).to_bytes(4,'little',signed = True)
            sinal_controle = b'\x01\x16\xd1\x08\x03\x02\x04' + valor_pid_binario
            sinal_controle_crc = calcula_CRC(sinal_controle, len(sinal_controle)).to_bytes(2,'little')
            uart.write(sinal_controle + sinal_controle_crc)

        
        #ESCREVE LOGS NO CSV
        with open('log1.csv','a') as csvfile:

            if valor_pid < 0:
                valor_ventoinha = valor_pid
                valor_resistor = 0
            else:
                valor_resistor = valor_pid
                valor_ventoinha = 0 

            mensagem = f'Temperatura Interna = {temp_interna[0]}, Temperatura Referencial = {temp_referencial[0]}, Temperatura Ambiente = {temp_ambiente},  Ventoinha = {valor_ventoinha}%, Resistor = {valor_resistor}%' 
            writer = csv.writer(csvfile,delimiter = ',')
            print(datetime.now().strftime('%d/%m/%Y %H:%M')+',',mensagem,file = csvfile)

        # LE COMANDOS DO USUARIO
        uart.write(le_usuario)
        recebe_uart = verifica_crc()

        if '0x0' != str(hex(recebe_uart[3])):

            if str(hex(recebe_uart[3])) == '0xa1':
                print('LIGOU FORNO')
                forno_estado = True
                uart.write(liga_forno)
                recebe_forno = verifica_crc()

            if str(hex(recebe_uart[3])) == '0xa2':
                print('DESLIGA FORNO')
                forno_estado = False
                uart.write(desliga_forno)
                recebe_forno = verifica_crc()
            
            if str(hex(recebe_uart[3])) == '0xa3' and forno_estado:
                print('INICIA AQUECIMENTO')
                inicia = True
                uart.write(inicia_aquecimento)
                recebe_forno = verifica_crc()

            if str(hex(recebe_uart[3])) == '0xa4':
                print('DESLIGA AQUECIMENTO')
                inicia = False
                uart.write(desliga_aquecimento)
                recebe_forno = verifica_crc()
                
            if str(hex(recebe_uart[3])) == '0xa5':
                print('MODO CURVA')
                if modo_curva == True:
                    uart.write(desliga_curva)
                    recebe_uart = verifica_crc()
                    modo_curva = False
                else:
                    uart.write(liga_curva)
                    recebe_uart = verifica_crc()
                    modo_curva = True
        
        time.sleep(1)

# Finaliza todo o sistema com o Ctrl + C 
except KeyboardInterrupt:

    uart.write(desliga_curva)
    uart.write(desliga_aquecimento)
    uart.write(desliga_forno)
    resistor_pwm.stop()
    ventoinha_pwm.stop()
    print('\nVentoinha,Resistor e todo o sistema desligado\n')
