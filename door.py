#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
from azure.iot.device import IoTHubDeviceClient

# Azure IoT Hub device connection string
CONNECTION_STRING = "Your Azure IoT Hub device connection string for door.py"

def iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def message_listener(client):
    door_status = "CLOSE DOOR"
    while True:
        try:
            message = client.receive_message()
            print(f"Received message: {message}")
            command = message.data.decode()

            if command == "OPEN":
                door_status = "OPEN DOOR"
                print(f"Door Status: {door_status}")
                time.sleep(5)  # Simulate the door opening for a period of time
                door_status = "CLOSE DOOR"

            print(f"Door Status: {door_status}")

        except Exception as e:
            print(f"Error receiving message: {e}")

def main():
    client = iothub_client_init()
    message_listener(client)

if __name__ == '__main__':
    main()



# In[ ]:




