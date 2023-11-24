#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import os
import threading
from azure.iot.device import IoTHubDeviceClient, Message

# Define connection strings for the client, door, and server
CLIENT_CONNECTION_STRING = "Your Azure IoT Hub device connection string for client.py"
DOOR_CONNECTION_STRING = "Your Azure IoT Hub device connection string for door.py"
SERVER_CONNECTION_STRING = "Your Azure IoT Hub device connection string for server.py"

# Dictionary to store employee information
employees = {}

# Flag to check if the server is running
server_running = False

# Server thread
server_thread = None

# Initialize IoT Hub client instances
client = IoTHubDeviceClient.create_from_connection_string(CLIENT_CONNECTION_STRING)
door_client = IoTHubDeviceClient.create_from_connection_string(DOOR_CONNECTION_STRING)
server_client = IoTHubDeviceClient.create_from_connection_string(SERVER_CONNECTION_STRING)

# Load employee information
def load_employees():
    global employees
    if os.path.exists("employees.json"):
        with open("employees.json", "r") as file:
            employees = json.load(file)
    else:
        employees = {}

# Save employee information
def save_employees():
    with open("employees.json", "w") as file:
        json.dump(employees, file)

# Initialize IoT Hub device client instance
def iothub_client_init(connection_string):
    client = IoTHubDeviceClient.create_from_connection_string(connection_string)
    return client

# Send a door opening command to the door device
def send_door_command(command, door_client):
    door_command = Message(command)
    door_client.send_message(door_command)
    print("Sent door command:", command)

# Handle punch-in data
def handle_punch_in_data(punch_in_data):
    name = punch_in_data["name"]
    employee_id = punch_in_data["employee_id"]
    if name in employees and employees[name] == employee_id:
        print(f"Welcome {name}, the door opens")
        # Send a door opening command to the door device
        send_door_command("OPEN", door_client)
    else:
        print("Error, please re-verify your identity")

# Receive messages from IoT Hub
def message_listener(client):
    global server_running
    while server_running:
        try:
            message = client.receive_message()
            print("Received message: {}".format(message))
            punch_in_data = json.loads(message.data.decode())
            handle_punch_in_data(punch_in_data)
        except Exception as e:
            print(f"Error receiving message: {e}")

# Show employee information
def show_employees():
    if employees:
        for name, employee_id in employees.items():
            print(f"Name: {name}, ID: {employee_id}")
    else:
        print("No employees added yet.")

# Add an employee
def add_employee():
    name = input("Enter employee name: ")
    employee_id = input("Enter employee ID: ")
    employees[name] = employee_id
    save_employees()
    print(f"Employee {name} added successfully.")

# Main menu
def main():
    global server_running, server_thread
    load_employees()

    while True:
        print("\nMain Menu")
        print("1. Add Employee")
        print("2. Show Employees")
        print("3. Start Server (Guard Mode)")
        print("4. Stop Server and Return to Menu")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_employee()
        elif choice == '2':
            show_employees()
        elif choice == '3':
            if server_thread and server_thread.is_alive():
                print("Server is already running.")
            else:
                server_running = True
                server_thread = threading.Thread(target=message_listener, args=(server_client,))
                server_thread.start()
        elif choice == '4':
            server_running = False
            if server_thread:
                server_thread.join()
            server_thread = None
            print("Returned to the main menu.")
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()




# In[ ]:




