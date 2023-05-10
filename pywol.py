#!/usr/bin/env python3

import json
import re
import paho.mqtt.client as mqtt
from wakeonlan import send_magic_packet

# Define MQTT broker details
broker_address = "192.168.22.5"
broker_port = 1883
topic = "muh/wol"

# Define MQTT client object
client = mqtt.Client()

# Define function to handle incoming MQTT messages
def on_message(client, userdata, message):
    data = json.loads(message.payload.decode())
    if message.topic == topic:
        try:
            if 'mac' in data:
                mac_address = data['mac']
                # Check MAC address format
                if len(mac_address) == 17 and re.match("^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac_address):
                    # Send WoL packet to MAC address
                    send_magic_packet(mac_address)
                    print(f"Sent WoL packet to MAC address {mac_address}")
                else:
                    print("Error: Incorrect MAC address format")
            else:
                print("Error: Payload does not contain MAC address")
        except Exception as e:
            print("Error: ", e)

# Set up MQTT client callbacks
client.on_message = on_message

# Connect to MQTT broker
print(f"Connecting to MQTT broker at {broker_address}:{broker_port}...")
client.connect(broker_address, broker_port)

# Subscribe to MQTT topic
print(f"Subscribing to MQTT topic {topic}...")
client.subscribe(topic)

# Start listening for MQTT messages
print("Listening for MQTT messages...")
client.loop_forever()
