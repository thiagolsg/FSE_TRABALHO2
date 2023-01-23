import struct
from crc import calcula_CRC

temp_interna = b'\x01\x23\xc1\x08\x03\x02\x04'
crc_tmp_interna = calcula_CRC(temp_interna, len(temp_interna)).to_bytes(2,'little')
solicita_temperatura_interna = temp_interna + crc_tmp_interna # Exportar essa variavel

temp_referencial = b'\x01\x23\xc2\x08\x03\x02\x04'
crc_tmp_referencial = calcula_CRC(temp_referencial, len(temp_referencial)).to_bytes(2,'little')
solicita_temperatura_referencial = temp_referencial + crc_tmp_referencial # Exportar essa variavel

le_usuario = b'\x01\x23\xc3\x08\x03\x02\x04'
crc_le_usuario = calcula_CRC(le_usuario, len(le_usuario)).to_bytes(2,'little')
le_usuario = le_usuario + crc_le_usuario # Exportar essa variavel

liga_forno = b'\x01\x16\xd3\x08\x03\x02\x04\x01'
liga_forno_crc = calcula_CRC(liga_forno, len(liga_forno)).to_bytes(2,'little')
liga_forno = liga_forno + liga_forno_crc # Exportar essa variavel

desliga_forno = b'\x01\x16\xd3\x08\x03\x02\x04\x00'
desliga_forno_crc = calcula_CRC(desliga_forno, len(desliga_forno)).to_bytes(2,'little')
desliga_forno = desliga_forno + desliga_forno_crc # Exportar essa variavel

inicia_aquecimento = b'\x01\x16\xd5\x08\x03\x02\x04\x01'
inicia_aquecimento_crc = calcula_CRC(inicia_aquecimento, 8).to_bytes(2,'little')
inicia_aquecimento = inicia_aquecimento + inicia_aquecimento_crc # Exportar essa variavel

desliga_aquecimento = b'\x01\x16\xd5\x08\x03\x02\x04\x00'
desliga_aquecimento_crc = calcula_CRC(desliga_aquecimento, 8).to_bytes(2,'little')
desliga_aquecimento = desliga_aquecimento + desliga_aquecimento_crc # Exportar essa variavel

liga_curva = b'\x01\x16\xd4\x08\x03\x02\x04\x01'
liga_curva_crc = calcula_CRC(liga_curva, len(liga_curva)).to_bytes(2,'little')
liga_curva = liga_curva + liga_curva_crc # Exportar essa variavel

desliga_curva = b'\x01\x16\xd4\x08\x03\x02\x04\x00'
desliga_curva_crc = calcula_CRC(desliga_curva, len(desliga_curva)).to_bytes(2,'little')
desliga_curva = desliga_curva + desliga_curva_crc # Exportar essa variavel

