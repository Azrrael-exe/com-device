import uvicorn
from fastapi import FastAPI

from serial import Serial
from llp import LLParser

uart = Serial("/dev/tty.usbmodem2143201", 115200, timeout=0.1)
app = FastAPI()
parser = LLParser(header=0x7e)

@app.get("/")
async def get_buffer():
    while uart.in_waiting > 0:
        message = uart.read_until()
        parser.parse(message)
    data = parser.get_buffer()
    return {"data": data}


@app.post("/")
async def post_buffer(data: dict):
    processed_data = {}
    for key, value in data.items():
        if key == "coffe":
            processed_data[0x0B] = value
        if key == "energy":
            processed_data[0x0A] = value
    encoded_message = parser.enconde(processed_data)
    uart.write(encoded_message)
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
