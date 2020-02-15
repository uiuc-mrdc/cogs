import serial
import serial.tools.list_ports
import sys

ser = [serial.serialposix.Serial(port=port.device, baudrate=9600, timeout=1) for port in serial.tools.list_ports.grep('PNP0501')]

buf = {}
for s in ser:
    s.reset_input_buffer()
    buf[s] = ''

try:
    while True:
        for s in ser:
            try:
                if s.in_waiting > 0:
                    read = s.read(1).decode('utf-8')
                    if read == '#' or read == '\n' or len(buf[s]) > 32:
                        print('{}: "{}"'.format(s.name, buf[s]))
                        buf[s] = ''
                    else:
                        buf[s] += read
            except Exception as e:
                print('Error on {}: {}'.format(s.name, e))
except KeyboardInterrupt:
    pass
