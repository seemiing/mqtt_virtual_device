import paho.mqtt.client as mqtt
import time
import threading
import random
from config import HOST, PORT, USERNAME, PASSWORD, SENSOR_INTERVAL_DELAY
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("lightpub")
    client.subscribe("fan")
    client.subscribe("ac")
    client.subscribe("Tony")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    message = msg.payload.decode("utf-8")
    topic = msg.topic
    
    if topic == "lightpub":
        if message == "On":
            client.publish("light_confirm", "Light is on")
        else:
            client.publish("light_confirm", "Light is off")
        print(f"Light: {message}")
    elif topic == "fan":
        if message == "On":
            client.publish("fan_confirm", "Fan is on")
        else:
            client.publish("fan_confirm", "Fan is off")
        print(f"Fan: {message}")
    elif topic == "ac":
        if message == "On":
            client.publish("AC_confirm", "AC is on")
        else:
            client.publish("AC_confirm", "AC is off")
        print(f"AC: {message}")
    else:
        print(topic + ": " + message)
def humidity_pub(mqttc):
    while True:
        mqttc.publish("humidity", random.randint(70, 100))
        time.sleep(SENSOR_INTERVAL_DELAY)

def temp_pub(mqttc):
    while True:
        mqttc.publish("temperature", random.randint(20, 36))
        time.sleep(SENSOR_INTERVAL_DELAY)

def light_pub(mqttc):
    while True:
        mqttc.publish("light", random.randint(0, 100))
        time.sleep(SENSOR_INTERVAL_DELAY)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.username_pw_set(USERNAME, PASSWORD)
mqttc.connect(HOST, PORT, 60)

mqttc.loop_start()

humid = threading.Thread(target=humidity_pub, args=(mqttc,))
humid.start()

temp = threading.Thread(target=temp_pub, args=(mqttc,))
temp.start()

light = threading.Thread(target=light_pub, args=(mqttc,))
light.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    mqttc.loop_stop()
    humid.join()
    temp.join()
    light.join()

