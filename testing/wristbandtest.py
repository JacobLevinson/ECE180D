import paho.mqtt.client as mqtt
import json
import math
import random
import speech_recognition as sr
import time
import multiprocessing
# Define mqtt server and topics
mqtt_server = 'mqtt.eclipseprojects.io'
led_controller_topic = 'ece180d/team3/reverseabomb/ledcontroller'
wristband1_topic = "ece180d/team3/reverseabomb/wristband1"
wristband2_topic = "ece180d/team3/reverseabomb/wristband2"

# functions for the client to puslish and subscribe data ************************


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(wristband1_topic, qos=1)


def on_message(client, userdata, msg):
    # Process incoming message
    topic = msg.topic
    wristband_id = topic.split('/')[-1]  # Extract wristband ID from topic
    message_content = str(msg.payload.decode(
        "utf-8")).upper()  # Assuming payload is text
    match message_content:
        case "SLAP1":
            print(f"SLAP received from wristband 1")
        case "SLAP2":
            print(f"SLAP received from wristband 2")


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect_async(mqtt_server)
    client.loop_start()
    while True:
        time.sleep(1)



if __name__ == "__main__":
    main()
