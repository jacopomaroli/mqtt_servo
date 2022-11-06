from msilib import sequence
import random
import time
import os
import json

from paho.mqtt import client as mqtt_client
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

broker = os.environ.get('BROKER')
port = int(os.environ.get('PORT'))
topic = os.environ.get('TOPIC')
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
client_id = f'python-mqtt-{random.randint(0, 100)}'

sequence = [
    {
        0: {
            "action": "rotate_absolute",
            "value": 125,
        },
        1: {
            "action": "rotate_absolute",
            "value": 125,
        }
    },
    {
        0: {
            "action": "rotate_relative",
            "value": 10,
        },
        1: {
            "action": "rotate_relative",
            "value": -10,
        }
    }
]


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    seq_idx = 0
    while True:
        if (seq_idx < len(sequence)):
            msg = json.dumps(sequence[seq_idx])
            result = client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")
            msg_count += 1
            seq_idx += 1
            time.sleep(3)


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
