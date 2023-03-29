#! /usr/bin/python3
#
# License: GNU General Public License (GPL) v.3
# http://www.gnu.org/licenses/gpl.html
# In short: don`t claim you wrote it, leave the copyright intact,
# give it away, modify it to fit your wishes, use it for whatever
# you want, but keep it free and the source code available.
#

"""
Started on 2020
@autor Pedro J. Bartolomey Nadal
Rutina que decodifica lo recibido por el multimetro.
"""
# import necessary modules
import re
import struct
import serial
import serial.tools.list_ports
import time
from time import sleep

# Routine: Check conexion with DMM.
def dmmcheck(port):
        # print (port)
        try:
            ser = serial.Serial(
            port=port,
            baudrate=2400,
            timeout = 0.1,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            rtscts=False,
            dsrdtr=True,
            bytesize=serial.EIGHTBITS
            )
            ser.close()
            ser.open()
            ser.flush()
            ser.setDTR(1)
            ser.setRTS(0)
            time.sleep(0.05)
            connectat=False
            for i in range(0,10):
                a=str(ser.readline())
                # print(i,a)
                if '+' in a or '-' in a:
                    connectat=True 
            if connectat:
                return(2)
            else:
                return(1)
        except:
            return(0)
        ser.close()


# Routine: Decode DMM input:
def dmmdecode(dmm_input):
    try:
        # print (dmm_input)
        value = int(dmm_input[1:5])
        divisor = int(dmm_input[6:7])
        if   (divisor == 0): divisor =    1 # 10e0
        elif (divisor == 4): divisor =   10 # 10e-1
        elif (divisor == 2): divisor =  100 # 10e-2
        elif (divisor == 1): divisor = 1000 # 10e-3
        else:
            # print ("Error: Unknown decimal position")
            divisor = 0
        value = value / divisor
        if (dmm_input[0:1].decode('ascii') == "-"):
            value *= -1
    except:
        value = "OVERFLOW"
    return (value)


# Routine: Return DMM flags:
def dmmflags(dmm_input):
    # print(format(int(dmm_input[0]), '08b'), end = '\t')
    # print(format(int(dmm_input[1]), '08b'), end = '\t')
    # print(format(int(dmm_input[2]), '08b'), end = '\t')
    # print(format(int(dmm_input[3]), '08b'), end = '\t')
    # print ('')
    flag_bits = (format(int(dmm_input[0]), '08b')) + (format(int(dmm_input[1]), '08b')) + (format(int(dmm_input[2]), '08b')) + (format(int(dmm_input[3]), '08b'))
    # print (flag_bits, type(flag_bits))

    # for cnt, x in enumerate(flag_bits):
    #   print("Bit {:2.0f}:\t {}".format(cnt, x))

    # Meaning of every bit
    # Bit Nr.             0       1       2       3       4       5       6       7
    # Byte 7 Symbol       0       0       Auto	DC      AC      REL     HOLD	BG
    # Bit Nr.             8       9       10      11      12      13      14      15
    # Byte 8 Symbol       0       0       MAX     MIN     0       LowBat	n       0
    # Bit Nr.             16      17      18      19      20      21      22      23
    # Byte 9 Symbol       µ       m       k       M       Beeps	Diode	%       0
    # Bit Nr.             24      25      26      27      28      29      30      31
    # Byte 10 Symbol      V       A       Ohm     0       Hz      F       °C      °F

    diccioflags = {'acdc':'', 'measure':'', 'prefijo':'', 'minmax':'', 'rel':'', 'hold':'', 'lowbat':'', 'range':'', 'buzz':'' }

    # range
    if (flag_bits[2] == '1'):  diccioflags.update({'range':'Autorange'})
    else:                      diccioflags.update({'range':'Manual'})
    # acdc
    if   (flag_bits[3] == '1') and (flag_bits[4] == '0'):   diccioflags.update({'acdc':'DC'})
    elif (flag_bits[3] == '0') and (flag_bits[4] == '1'):   diccioflags.update({'acdc':'AC'})
    else:                                                   diccioflags.update({'acdc':'--'})
    # REL
    if (flag_bits[5] == '1'):  diccioflags.update({'rel':'REL'})            # 1 = REL
    else:                      diccioflags.update({'rel':'--'})
    # HOLD
    if (flag_bits[6] == '1'):  diccioflags.update({'hold':'HOLD'})          # 1 = HOLD
    else:                      diccioflags.update({'hold':'--'})
    # minmax
    if   (flag_bits[10] == '1') and (flag_bits[10] == '0'):   diccioflags.update({'minmax':'MAX'})
    elif (flag_bits[11] == '0') and (flag_bits[11] == '1'):   diccioflags.update({'minmax':'MIN'})
    else:                                                     diccioflags.update({'minmax':'--'})
    # lowbat
    if (flag_bits[13] == '1'): diccioflags.update({'lowbat':'LOWBAT'})      # 1 = low battery warning
    else:                      diccioflags.update({'lowbat':'BAT-OK'})
    # prefijo
    if   (flag_bits[14] == '1'): prefijo = 'n'                              # 1 = nano		10e-9
    elif (flag_bits[16] == '1'): prefijo = 'µ'                              # 1 = micro / u / µ	10e-6
    elif (flag_bits[17] == '1'): prefijo = 'm'                              # 1 = milli		10e-3
    elif (flag_bits[18] == '1'): prefijo = 'k'                              # 1 = kilo		10e3
    elif (flag_bits[19] == '1'): prefijo = 'M'                              # 1 = Mega		10e6
    else:                        prefijo = ''
    if   (flag_bits[20] == '1'): 
        measure = 'Ω'                                                       # 1 = continuity buzzer
        diccioflags.update({'buzz':'BUZZ'})
    elif (flag_bits[21] == '1'): 
        measure = 'V'                                                       # 1 = diode check
        diccioflags.update({'buzz':'DIODE'})
    elif (flag_bits[22] == '1'): measure = '%'                              # 1 = duty cycle
    elif (flag_bits[24] == '1'): measure = 'V'                              # 1 = voltage 
    elif (flag_bits[25] == '1'): measure = 'A'                              # 1 = current
    elif (flag_bits[26] == '1'): measure = 'Ω'                              # 1 = resistance
    elif (flag_bits[28] == '1'): measure = 'Hz'                             # 1 = frequency
    elif (flag_bits[29] == '1'): measure = 'F'                              # 1 = capacity Farad and prefixes not tested!!!
    elif (flag_bits[30] == '1'): measure = '°C'                             # 1 = temperature, deg/° Celsius
    elif (flag_bits[31] == '1'): measure = '°F'                             # 1 = temperature, deg/° Fahrenheit
    else:                        measure = '--'
    diccioflags.update({'measure':prefijo + measure})
    return (diccioflags)
