import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from threading import Thread
from json import dumps
import paho.mqtt.client as mqtt
from time import sleep

from serial import Serial
from llp import LLParser

uart = Serial("/dev/tty.usbmodem2143401", 115200, timeout=0.1)
app = FastAPI()
parser = LLParser(header=0x7e)

client = mqtt.Client()

client.connect("test.mosquitto.org", 1883, 60)
client.subscribe("alico/fundas/nevera/input")

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


@app.get("/status")
async def get_status():    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hello World</title>
    </head>
    <body>
        <h1>Hello, World!</h1>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

def run_serial():
    while True:
        client.loop(timeout=1.0, max_packets=1)
        while uart.in_waiting > 0:
            message = uart.read_until()
            parser.parse(message)
            data = parser.get_buffer()
            client.publish(topic="alico/fundas/nevera", payload=dumps(data), qos=0, retain=False)
        sleep(0.1)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client.on_message = on_message

if __name__ == "__main__":
    pusblishe_thread = Thread(target=run_serial)
    pusblishe_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
