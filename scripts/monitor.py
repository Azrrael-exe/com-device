from serial import Serial
from time import sleep
from llp import LLParser

uart = Serial("/dev/tty.usbmodem2143201", 115200, timeout=0.1)

parser = LLParser(header=0x7e)
        
while True:
    variable_name = input("Enter Variable Name: ")
    if variable_name == "Coffe":
        value = int(input("Enter Value: "))
        payload = {0x0B: value}
        uart.write(parser.enconde(payload=payload))
    
    if variable_name == "Energy":
        value = int(input("Enter Value: "))
        payload = {0x0A: value}
        uart.write(parser.enconde(payload=payload))

    if uart.in_waiting > 0:
        message = uart.read_until()
        parser.parse(message)
    
    if parser.available() > 1:
        data = parser.get_buffer()
        for sample in data:
            print(sample)