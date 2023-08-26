from serial import Serial

class Datapack:
    def __init__(self, uart: Serial, header: int):
        self.__uart = uart
        self.__header = header
        self.__data = {}


    def available(self) -> bool:
        if self.__uart.in_waiting > 0:
            input = ord(self.__uart.read())
            if input == self.__header:
                lenght = ord(self.__uart.read())
                payload = []
                for i in range(0, lenght):
                    payload.append(self.__uart.read())
                rec_checksum = ord(self.__uart.read())

            output = {}
            for i in range(0, int(len(payload) / 3)):
                output[hex(ord(payload[i * 3]))] = [payload[(i*3) + 1],  payload[(i*3) + 2]]
            self.__data = {**self.__data, **output}
            return True
        
        return False
    
    def read(self) -> dict:
        return self.__data
    