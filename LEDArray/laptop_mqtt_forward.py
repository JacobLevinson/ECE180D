import serial
import serial.tools.list_ports
import time
import paho.mqtt.client as mqtt

# Define MQTT server and topic
mqtt_server = 'mqtt.eclipseprojects.io'
led_controller_topic = 'ece180d/team3/reverseabomb/ledcontroller'

# Find Arduino port


def find_arduino():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'Arduino' in port.description or 'tty.usbmodem' in port.device or 'tty.usbserial' in port.device:
            return port.device
    return None


arduino_port = find_arduino()

if arduino_port is None:
    print("Arduino not found. Please check the connection.")
else:
    print(f"Arduino found on port: {arduino_port}")
    baud_rate = 9600
    ser = serial.Serial(arduino_port, baud_rate)
    time.sleep(2)  # Wait for the connection to establish

    def send_data_to_arduino(data):
        ser.write(data.encode())
        print(f"Sent to Arduino: {data}")

    # Define the callback functions for MQTT
    def on_connect(client, userdata, flags, rc):
        """Callback for when the client receives a CONNACK response from the server."""
        print(f"Connected to MQTT server with result code {rc}")
        client.subscribe(led_controller_topic)

    def on_message(client, userdata, msg):
        """Callback for when a PUBLISH message is received from the server."""
        message = msg.payload.decode()
        print(f"Received message: {message} on topic: {msg.topic}")
        send_data_to_arduino(message)

    # Create an MQTT client instance
    client = mqtt.Client()

    # Assign the callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT server
    client.connect(mqtt_server, 1883, 60)

    # Start the loop to process network traffic and dispatch callbacks
    client.loop_start()

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
        client.loop_stop()
        ser.close()
