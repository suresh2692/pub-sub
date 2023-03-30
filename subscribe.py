import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))

 
MQTT_HOST = "broker.hivemq.com"
MQTT_TOPIC = "hiphop2025"
MQTT_PORT = 1883
client = mqtt.Client("receiver")
client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_start()
client.subscribe(MQTT_TOPIC)
while True: 
    client.on_message=on_message 
    # client.loop_stop()
    #client.disconnect()
    time.sleep(3)
    