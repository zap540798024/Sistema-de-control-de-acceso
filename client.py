#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import time
from azure.iot.device import IoTHubDeviceClient, Message

# Azure IoT Hub device connection string
CONNECTION_STRING = "Your Azure IoT Hub device connection string"

# Create an IoT Hub device client instance
def iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def send_punch_in_data(client, name, employee_id):
    punch_in_data = {
        "name": name,
        "employee_id": employee_id,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    message = Message(json.dumps(punch_in_data))
    print("Sending message: {}".format(message))
    client.send_message(message)
    print("Message successfully sent")

def main():
    client = iothub_client_init()
    try:
        while True:
            name = input("Enter employee name: ")
            employee_id = input("Enter employee ID: ")
            send_punch_in_data(client, name, employee_id)

    except KeyboardInterrupt:
        print("Simulation stopped")
        client.disconnect()

if __name__ == "__main__":
    main()

