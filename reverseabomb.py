import paho.mqtt.client as mqtt
import json


sensor_data = {
    "wristband1": {"ACC_X": None, "ACC_Y": None, "ACC_Z": None, "GYR_X": None, "GYR_Y": None, "GYR_Z": None},
    "wristband2": {"ACC_X": None, "ACC_Y": None, "ACC_Z": None, "GYR_X": None, "GYR_Y": None, "GYR_Z": None},
}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("ece180d/team3/reverseabomb/wristband1", qos=1)
    client.subscribe("ece180d/team3/reverseabomb/wristband2", qos=1)


def on_message(client, userdata, msg):
    # Process incoming message
    topic = msg.topic
    wristband_id = topic.split('/')[-1]  # Extract wristband ID from topic
    try:
        # Decode JSON payload
        data = json.loads(msg.payload.decode())
        # Validate and update the global structure with the new data
        if all(key in data for key in ["ACC_X", "ACC_Y", "ACC_Z", "GYR_X", "GYR_Y", "GYR_Z"]):
            sensor_data[wristband_id].update({
                "ACC_X": data["ACC_X"], "ACC_Y": data["ACC_Y"], "ACC_Z": data["ACC_Z"],
                "GYR_X": data["GYR_X"], "GYR_Y": data["GYR_Y"], "GYR_Z": data["GYR_Z"]
            })
            print(f"Updated {wristband_id} data: {sensor_data[wristband_id]}")
        else:
            print(f"Received data does not contain all required fields for
                   {wristband_id}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {wristband_id}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect_async('mqtt.eclipseprojects.io')
    client.loop_start()


if __name__ == "__main__":
    main()
