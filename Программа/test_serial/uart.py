import serial
from typing import Literal, Any


class BaseCommand:
    name: str = 'command'
    parametrs_name: list = ['arg1', 'arg2', 'arg3']
    allowed_types_short_answer: tuple = ('OK', 'Error')

    def command_to_str(name, **kwargs) -> str:
        pass

    def parse_short_answer(s: str) -> bool:
        pass

    def parse_long_answer(s: str) -> list:
        pass


class SetupCommand(BaseCommand):
    name: str = 'setup'
    parametrs_name: tuple = ('pk', 'ik', 'dk', 'minch')
    allowed_types_short_answer: tuple = ('OK', 'Error')

    def command_to_str(args: dict) -> str:
        s: str = ''
        s += SetupCommand.name
        end_i = len(args)-1
        for i, (key, value) in enumerate(args.items()):
            if i == 0:
                s += ' '
            if key not in SetupCommand.parametrs_name:
                raise 'Not correct argument'
            s += f'{key} : {value}'
            if i != end_i:
                s += ', '
        s += '\n'
        return s

    def parse_short_answer(s: str) -> bool:
        name, value = s.replace('\n', '').split(' : ')
        if (name == 'status') and (value in SetupCommand.allowed_types_short_answer):
            if (value == 'OK'):
                return True
            elif (value == 'Error'):
                return False
        else:
            raise 'Not correct short answer'


class ImuCommand(BaseCommand):
    name: str = 'imu'
    parametrs_name: tuple = ('turn')
    allowed_types_short_answer: tuple = ('OK', 'Error')

    def command_to_str(args: dict) -> str:
        s: str = ''
        s += SetupCommand.name
        end_i = len(args)-1
        for i, (key, value) in enumerate(args.items()):
            if i == 0:
                s += ' '
            if key not in SetupCommand.parametrs_name:
                raise 'Not correct argument'
            s += f'{key} : {value}'
            if i != end_i:
                s += ', '
        s += '\n'
        return s

    def parse_short_answer(s: str) -> bool:
        name, value = s.replace('\n', '').split(' : ')
        if (name == 'status') and (value in SetupCommand.allowed_types_answer):
            if (value == 'OK'):
                return True
            elif (value == 'Error'):
                return False
        else:
            raise 'Not correct short answer'


class PostmanUart:
    def __init__(self, port: str, baudrate: int, struct: Any):
        self.port = port
        self.baudrate = baudrate
        self.struct = struct
        self.serial = serial.Serial()

    def configure(self, **kwargs):
        self.disconnect()
        self.serial.apply_settings(kwargs)

    def connect(self):
        if not self.serial.is_open:
            self.serial.open()

    def disconnect(self):
        if self.serial.is_open:
            self.serial.close()

    def write(self, message: bytes) -> bool:
        result = None
        try:
            result = self.serial.write(message)
        except serial.SerialTimeoutException as e:
            return False
        if result is None:
            return False
        else:
            return True

    def bulid_command_imu(self, turn: bool):
        s: str = ''
        s += 'imu' + ' '
        s += f'turn : {turn}'
        s += '\n'
        return s

    def write_command(self, command_title: Literal['setup', 'imu'], **kwargs):
        if command_title == 'setup':
            command_str = self.bulid_command_setup()
            result = self.write(command_str)

        elif command_title == 'imu':
            command_str = self.bulid_command_imu()
            result = self.write(command_str)

    def listen_short(self):
        s = self.serial.readline().decode('utf-8')

    def parse_short_answer(self, s: str):
        command_title, command_val = " : ".split(s)

    def struct_to_list(self) -> list:
        if type(self.struct) == dict:
            l = []
            for arg, val in self.struct.items():
                l.append(f'{arg}:{val}')
            return l
        else:
            raise 'Not allowed types of structure for uart receiver'

    def str_to_struct(self): ...


COM_PORT = "COM1"
# Открываем Serial порт ('COMX' замените на имя вашего порта)
ser = serial.Serial('COMX', 115200)
# Отправляем строку "Hello, Arduino!" на Arduino, предварительно преобразовав ее в байты
ser.write(b'Hello, Arduino!')
# Читаем ответ от Arduino через Serial порт
response = ser.readline()
# Декодируем ответ из байтов в строку с использованием UTF-8
decoded_response = response.decode('utf-8')
# Закрываем порт
ser.close()
print(decoded_response)
