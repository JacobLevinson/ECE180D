import paho.mqtt.client as mqtt
import time
import random

# Define MQTT parameters
mqtt_server = 'mqtt.eclipseprojects.io'
led_controller_topic = 'ece180d/team3/reverseabomb/ledcontroller'

# Define LED strip parameters
LED_STRIP_LENGTH = 11

# Define the MQTT client
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection. Reconnecting...")
        print("Reason code:", rc)
        client.reconnect()

def send_led_state(client, led_position):
    # Convert the LED positions list to a comma-separated string
    led_state_str = ''.join(led_position)
    
    # Publish the LED state to the LED controller topic with QoS 0
    client.publish(led_controller_topic, led_state_str, qos=0)
    print("LED state published to the LED controller topic.")
    print("LED positions:", led_position)  # Print LED positions for debugging


def main():
    # Set MQTT callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    # Connect to MQTT broker
    client.connect(mqtt_server, 1883)

    try:
        while True:
            # Generate LED positions
            led_position = ['b'] * LED_STRIP_LENGTH
            red_index = random.randint(0, LED_STRIP_LENGTH - 1)
            led_position[red_index] = 'r'  # Set one LED to red

            # Send LED state
            send_led_state(client, led_position)

            # Wait for a while before sending the next state
            time.sleep(2)

    except KeyboardInterrupt:
        # Disconnect from MQTT broker
        client.disconnect()
        print("Disconnected from MQTT broker.")

if __name__ == "__main__":
    main()
