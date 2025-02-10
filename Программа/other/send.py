import serial
from serial.tools import list_ports
from json import load as JSON_load
import time
import win32api
import sys
import glob


def serial_ports():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


with open("data.json", 'r') as file:
    data = JSON_load(file)
    print(data)
    #print(data['v'])

'''
data={x=float,
z=float,
n=int,
v=int}
'''

data2 = [((3 - len(data['x'][:data['x'].find('.')])) * '0') + data['x'] +
         ((5 - len(data['x'][data['x'].find('.') + 1:])) * '0'),

         ((3 - len(data['z'][:data['z'].find('.')])) * '0') + data['z'] +
         ((5 - len(data['z'][data['x'].find('.') + 1:])) * '0'),

         data['n'],

         ((4 - len(data['v'])) * '0') + str(data['v'])]
print(data2)

#list_com = list_ports.comports()
serial_ports = serial_ports()
print(serial_ports)

for i in range(len(serial_ports)):
    try:
        ser = serial.Serial(serial_ports[i], 9600)
        time.sleep(2)
        ser.reset_input_buffer()

        ser.write(data2[0] .encode())
        ser.write(data2[1].encode())
        ser.write(data2[2] .encode())
        ser.write(data2[3].encode())
    except Exception as e:
        win32api.MessageBox(0, 'Ошибка загрузки', 'Ошибка', 0x00000010)
        print(e)
        exit()
    #ser.write(b'helo')
    time.sleep(4)
    #ser.close()
if len(serial_ports) == 0:
    win32api.MessageBox(0, 'Устройство не найдено', 'Ошибка', 0x00000010)
else:
    win32api.MessageBox(0, 'Загрузка произошла успешно', 'Оповещение', 0x00000040)

