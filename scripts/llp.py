
class LLParser:
    def __init__(self, header: int):
        self._header = header
        self._buffer = []
        self._parsed_buffer = []
    
    def available(self) -> int:
        return len(self._parsed_buffer)

    def get_buffer(self) -> list[dict[str, int]]:
        buffer = self._parsed_buffer
        self._parsed_buffer = []
        return buffer

    def parse(self, message: bytes) -> None:
        self._buffer += message
        while len(self._buffer) > 0:
            try:
                header = self._buffer.pop(0)

                if header == self._header:
                    output = {}
                    length = self._buffer.pop(0)
                    payload = [self._buffer.pop(0) for _ in range(length)]
                    received_checksum = self._buffer.pop(0)
                    checksum = 0
                    for b in payload:
                        checksum += b
                    checksum = (0xFF - checksum) % 256
                    try:
                        assert checksum == received_checksum
                    except AssertionError as e:
                        print(f"Invalid checksum received: {received_checksum} != {checksum}")
                        raise e
                    
                    for i in range(int(len(payload) / 3)):
                        output[payload[i * 3]] = (payload[(i * 3) + 1] << 8) + payload[(i * 3) + 2]
                    self._parsed_buffer.append(output)
            except IndexError as e:
                break
    
    
    def enconde(self, payload: dict[int, int]) -> list[int]:
        header = [self._header, len(payload) * 3]
        enconded_payload = []
        for key, value in payload.items():
            enconded_payload.append(key)
            enconded_payload.append(value >> 8)
            enconded_payload.append(value & 0xFF)

        checksum = (0xFF - sum(enconded_payload)) % 256


        return header + enconded_payload + [checksum]


