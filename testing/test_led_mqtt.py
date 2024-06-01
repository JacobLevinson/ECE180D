import paho.mqtt.client as mqtt

# Define MQTT server and topic
mqtt_server = 'mqtt.eclipseprojects.io'
led_controller_topic = 'ece180d/team3/reverseabomb/ledcontroller'

# Define the callback functions


def on_connect(client, userdata, flags, rc):
    """Callback for when the client receives a CONNACK response from the server."""
    print(f"Connected with result code {rc}")
    client.subscribe(led_controller_topic)


def on_message(client, userdata, msg):
    """Callback for when a PUBLISH message is received from the server."""
    print(f"Received message: {msg.payload.decode()} on topic: {msg.topic}")


# Create an MQTT client instance
client = mqtt.Client()

# Assign the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT server
client.connect(mqtt_server, 1883, 60)

# Start the loop to process network traffic and dispatch callbacks
client.loop_forever()
