from dotenv import load_dotenv
load_dotenv()

from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi import FastAPI
from fastapi_mqtt.config import MQTTConfig

from fastapi.middleware.cors import CORSMiddleware
from os import environ

from src.backend.routers import (
    ping_router,
    auth_router,
    admin_router
)

app = FastAPI(title="IOTProject")

config = {}

mqtt_config = MQTTConfig(host=environ["MQTT_HOST"], port=int(environ["MQTT_PORT"]))

mqtt = FastMQTT(config=mqtt_config)

mqtt.init_app(app)

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/mqtt") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)
    return 0

@mqtt.subscribe("/mqtt")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


@app.get("/publishmqtt")
async def func():
    mqtt.publish("/mqtt", "Hello from Fastapi") #publishing mqtt topic
    return {"result": True,"message":"Published" }

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ping_router.router)
app.include_router(auth_router.router)
app.include_router(admin_router.admin_router)

