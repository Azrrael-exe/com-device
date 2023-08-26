from serial import Serial
from time import sleep
from llp import Datapack

uart = Serial("/dev/tty.usbmodem1101", 115200)

pack = Datapack(uart=uart, header=0x7e)

while True:
    if pack.available():
        message = pack.read()
        if message.get("0xa1"):
            print(message)
    sleep(0.1)
