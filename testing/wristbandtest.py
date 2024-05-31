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
