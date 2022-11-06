import random
import os
import json

from adafruit_servokit import ServoKit
from paho.mqtt import client as mqtt_client
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)

broker = os.environ.get('BROKER')
port = int(os.environ.get('PORT'))
topic = os.environ.get('TOPIC')
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
client_id = f'python-mqtt-{random.randint(0, 100)}'


def rotate_absolute(motor_idx, motor_angle):
    try:
        kit.servo[motor_idx].angle = motor_angle
    except Exception as e:
        print(e)


def rotate_relative(motor_idx, motor_angle):
    try:
        kit.servo[motor_idx].angle += motor_angle
    except Exception as e:
        print(e)


action_map = {
    "rotate_absolute": rotate_absolute,
    "rotate_relative": rotate_relative
}


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    print(f"Connecting to broker \"{broker}\"...\n")
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        msg_payload_json = msg.payload.decode()
        print(f"Received `{msg_payload_json}` from `{msg.topic}` topic")
        msg_payload = {}
        try:
            msg_payload = json.loads(msg_payload_json)
        except Exception as e:
            print(e)
        for motor in msg_payload.keys():
            motor_idx = int(motor)
            action = msg_payload[motor]["action"]
            value = msg_payload[motor]["value"]
            action_fn = action_map.get(action)
            if (action_fn):
                action_fn(motor_idx, value)

    client.subscribe(topic)
    client.on_message = on_message


def calibrate():
    for motor_idx in range(0, 16):
        kit.servo[motor_idx].angle = 0


def run():
    calibrate()
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
