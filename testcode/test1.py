from netmiko import ConnectHandler
import re
import random
from pymongo import MongoClient
# Cisco device SSH connection details
device = {
            'device_type': 'cisco_ios',
            'ip': '10.1.44.105',  # IP address of the Cisco device
            'username': 'admin',
            'password': 'MFUschl123',
            }


# Connect to the Cisco WLC
net_connect = ConnectHandler(**device)

output = net_connect.send_command("show wlan summary")

# Disconnect from the Cisco WLC
net_connect.disconnect()

wlan_ids = []
lines = output.splitlines()
print(lines)
for line in lines[5:]:
    if line.strip():
        match = re.match(r'^\s*(\d+)', line)
        if match:
            wlan_id = match.group(1)
            wlan_ids.append(wlan_id)

# Print the WLAN IDs
for wlan_id in wlan_ids:
    print(wlan_id)
    
existing_array = [None] * 15

# Your code to retrieve WLAN IDs and store them in wlan_ids list


# Add the values from wlan_ids to the existing array
for i in range(len(wlan_ids)):
    existing_array[i] = wlan_ids[i]

# Print the updated array
print(existing_array) 

next_position = existing_array.index(None)

# Generate a random number between 1 and 16
random_num = random.randint(1, 16)

# Check if the random number already exists in the array
while str(random_num) in existing_array:
    random_num = random.randint(1, 16)  # Generate a new random number

# Replace the next available position with the random number
existing_array[next_position] = str(random_num)

print(existing_array)  # Print the updated array  

next_position = existing_array.index(None)

# Generate a random number between 1 and 16
random_num = random.randint(1, 16)

# Check if the random number already exists in the array
while str(random_num) in existing_array:
    random_num = random.randint(1, 16)  # Generate a new random number

# Replace the next available position with the random number
existing_array[next_position] = str(random_num)

print(existing_array)  # Print the updated array  
print(random_num)