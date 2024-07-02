from flask import (
    Flask,
    request,
    send_from_directory,
    render_template,
    redirect,
    url_for,
    jsonify,
)
import datetime
from netmiko import ConnectHandler
import re
import random
from pymongo import MongoClient
import os
<<<<<<< HEAD
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, NTLM
=======
>>>>>>> 050c80309c89a3e7e25dd8f416a7ae65b3e6b011

current_time = datetime.datetime.now()

# ปรับเปลี่ยนเป็นพุทธศักราช
buddhist_year = current_time.year + 543

# สร้างวัตถุ datetime ใหม่ที่มีการเปลี่ยนแปลงแล้ว
buddhist_time = current_time.replace(year=buddhist_year)
# แสดงวันที่แบบพุทธศักราช
formatted_time = buddhist_time.strftime("%Y-%m-%d %H:%M:%S")

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    with open("tester.html", "r", encoding="utf-8") as file:
        return file.read()

@app.route('/testtest.html', methods=['GET'])
def testtest():
    return send_from_directory('.', 'testtest.html')




@app.route("/testest", methods=["GET"])
def testpage():
    with open("testtest.html", "r", encoding="utf-8") as file:
        return file.read()


# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["mydb"]
collection = db["ssid"]


@app.route("/history", methods=["GET"])
def history():
    # Retrieve data from MongoDB
    data = collection.find()
    documents = list(data)

    # Render the template and pass the retrieved data
    return render_template("/history.html", documents=documents)


@app.route("/configure_ssid1", methods=["POST"])  # ไม่มีรหัสผ่าน
def configure_ssid1():
    ssid1 = request.form["ssid1"]
    event1 = request.form["event1"]
    location1 = request.form["location1"]
    post(ssid1, event1, location1)

    device = {
        "device_type": "cisco_ios",
        "ip": "172.30.99.56",
        "username": "admin",
        "password": "CITS@WLC2023",
        "secret": "CITS@WLC2023",
    }

    # Connect to the Cisco device
    net_connect = ConnectHandler(**device)
    oo = net_connect.enable()
    # Send the command
    print(oo)

    output = net_connect.send_command("show wlan summary")

    wlan_ids = []
    lines = output.splitlines()
    print(lines)
    for line in lines[5:]:
        if line.strip():
            match = re.match(r"^\s*(\d+)", line)
            if match:
                wlan_id = match.group(1)
                wlan_ids.append(wlan_id)

    # Print the WLAN IDs
    for wlan_id in wlan_ids:
        print(wlan_id)

    existing_array = [None] * 15

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

    config_commands = [
        f"wlan {ssid1} {random_num} {ssid1}",
        f"no security wpa",
        f"no shutdown",
        f"exit",
        f"wireless tag policy {location1}",
        f"wlan {ssid1} policy MFUPolicyProfile1",
        f"end",
    ]

    output = net_connect.send_config_set(config_commands)
    print(output)

    # Disconnect from the Cisco device
    net_connect.disconnect()

    return redirect(url_for("history"))


@app.route("/configure_ssid", methods=["POST"])  # รหัสผ่านร่วมกัน
def configure_ssid():
    ssid = request.form["ssid"]
    password = request.form["password"]
    event = request.form["event"]
    location = request.form["location"]
    post(ssid, event, location)

    device = {
        "device_type": "cisco_ios",
        "ip": "172.30.99.56",
        "username": "admin",
        "password": "CITS@WLC2023",
        "secret": "CITS@WLC2023",
    }

    # Connect to the Cisco device
    net_connect = ConnectHandler(**device)
    oo = net_connect.enable()
    # Send the command
    print(oo)

    output = net_connect.send_command("show wlan summary")

    wlan_ids = []
    lines = output.splitlines()
    print(lines)
    for line in lines[5:]:
        if line.strip():
            match = re.match(r"^\s*(\d+)", line)
            if match:
                wlan_id = match.group(1)
                wlan_ids.append(wlan_id)

    # Print the WLAN IDs
    for wlan_id in wlan_ids:
        print(wlan_id)

    existing_array = [None] * 15

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

    config_commands = [
        f"wlan {ssid} {random_num} {ssid}",
        f"security ft",
        f"security wpa psk set-key ascii 0 {password} {password}",
        f"no security wpa akm dot1x",
        f"security wpa akm psk",
        f"security wpa akm ft psk",
        f"no shutdown",
        f"exit",
        f"wireless tag policy {location}",
        f"wlan {ssid} policy MFUPolicyProfile1",
        f"end",
    ]

    output = net_connect.send_config_set(config_commands)
    print(output)

    # Disconnect from the Cisco device
    net_connect.disconnect()

    return redirect(url_for("history"))


@app.route("/configure_ssid2", methods=["POST"])  # แบบรายบุคคล
def configure_ssid2():
    ssid2 = request.form["ssid2"]
    event2 = request.form["event2"]
    location2 = request.form["location2"]
    csv_file = request.files["csvFile"]

    # Save the event details into the ssid collection
    ssid_id = post(ssid2, event2, location2)

    # Save CSV file to a directory
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    csv_filename = os.path.join("uploads", csv_file.filename)
    csv_file.save(csv_filename)

    # Connect to the MongoDB server
    client = MongoClient("mongodb://localhost:27017")
    db = client["mydb"]
    history_collection = db["history"]

    # Process CSV file and insert data into MongoDB
    import csv

    users = []
    with open(csv_filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if (
                len(row) == 3
            ):  # Assuming the CSV has 3 columns: name, ID card number, phone number
                user = {
                    "ssid_id": ssid_id,
                    "name": row[0],
                    "id_card_number": row[1],
                    "phone_number": row[2],
                }
                users.append(user)

    # Insert all users into the MongoDB collection
    if users:
        history_collection.insert_many(users)
        print(f"Inserted users: {users}")
    else:
        print("No users found in CSV file.")

    device = {
        "device_type": "cisco_ios",
        "ip": "172.30.99.56",
        "username": "admin",
        "password": "CITS@WLC2023",
        "secret": "CITS@WLC2023",
    }

    # Connect to the Cisco device
    net_connect = ConnectHandler(**device)
    oo = net_connect.enable()
    # Send the command
    print(oo)

    output = net_connect.send_command("show wlan summary")

    wlan_ids = []
    lines = output.splitlines()
    print(lines)
    for line in lines[5:]:
        if line.strip():
            match = re.match(r"^\s*(\d+)", line)
            if match:
                wlan_id = match.group(1)
                wlan_ids.append(wlan_id)

    # Print the WLAN IDs
    for wlan_id in wlan_ids:
        print(wlan_id)

    existing_array = [None] * 15

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

    config_commands = [
        f"wlan {ssid2} {random_num} {ssid2}",
        f"no security ft adaptive",
        f"security dot1x authentication-list list",
        f"security ft",
        f"security wpa akm ft dot1x",
        f"no shutdown",
        f"exit",
        f"wireless tag policy {location2}",
        f"wlan {ssid2} policy MFUPolicyProfile1",
        f"end",
    ]

    output = net_connect.send_config_set(config_commands)
    print(output)

    # Disconnect from the Cisco device
    net_connect.disconnect()

    return redirect(url_for("history"))


def post(ssid, event, location):
    current_time = datetime.datetime.now()

    # ปรับเปลี่ยนเป็นพุทธศักราช
    buddhist_year = current_time.year + 543

    # สร้างวัตถุ datetime ใหม่ที่มีการเปลี่ยนแปลงแล้ว
    buddhist_time = current_time.replace(year=buddhist_year)
    # แสดงวันที่แบบพุทธศักราช
    formatted_time = buddhist_time.strftime("%Y-%m-%d %H:%M:%S")

    # Connect to the MongoDB server
    client = MongoClient("mongodb://localhost:27017")

    # Access the database
    db = client["mydb"]

    # Access the collection
    collection = db["ssid"]

    # Create a document to insert
    document = {
        "ssid": ssid,
        "event": event,
        "location": location,
        "time": formatted_time,
    }

    # Insert the document into the collection
    result = collection.insert_one(document)

    # Close the MongoDB connection
    client.close()

    # Return the id of the inserted document
    return result.inserted_id

<<<<<<< HEAD

@app.route("/delete_ssid/<ssid_id>", methods=["DELETE"])
=======
@app.route('/delete_ssid/<ssid_id>', methods=['DELETE'])
>>>>>>> 050c80309c89a3e7e25dd8f416a7ae65b3e6b011
def delete_ssid(ssid_id):
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017")
    db = client["mydb"]
    collection = db["ssid"]

    # Get the location from the MongoDB document
    ssid_document = collection.find_one({"ssid": ssid_id})
    location = ssid_document["location"]

    device = {
        "device_type": "cisco_ios",
        "ip": "172.30.99.56",
        "username": "admin",
        "password": "CITS@WLC2023",
        "secret": "CITS@WLC2023",
    }

    # Connect to the Cisco device
    net_connect = ConnectHandler(**device)
    oo = net_connect.enable()

    print(oo)

    # Send the command to delete the SSID on the WLC
    config_commands = [
        f"no wlan {ssid_id}",
        f"wireless tag policy {location}",
        f"no wlan {ssid_id} policy MFUPolicyProfile1",
        f"end",
    ]

    output = net_connect.send_config_set(config_commands)
    print(output)

    # Disconnect from the Cisco device
    net_connect.disconnect()

    # Delete the SSID document from the collection
    result = collection.delete_one({"ssid": ssid_id})

    if result.deleted_count == 1:
        return "SSID deleted successfully!"
    else:
        if "writeErrors" in result.raw_result:
            error_message = (
                f'Failed to delete SSID. Error: {result.raw_result["writeErrors"]}'
            )
        else:
            error_message = "Failed to delete SSID."

        return error_message


# Serve static files from the 'static' folder
@app.route("/static/<path:filename>", methods=["GET"])
def serve_static(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, "static"), filename)


if __name__ == "__main__":
    app.run(host="localhost", port=3000)


# add user in ad


app = Flask(__name__)

domain = "test"
loginun = "Administrator"
loginpw = "12345678Xx"


@app.route("/add_user", methods=["POST"])
def add_user():
    username = request.json.get("username")
    useremail = request.json.get("useremail")
    userpswd = request.json.get("userpswd")
    userdn = request.json.get("userdn")
    group_dn = request.json.get("group_dn")

    # Connect to LDAP server
    s = Server("ldaps://10.1.55.210:636", connect_timeout=5, use_ssl=True, get_info=ALL)
    c = Connection(s, user="test\\Administrator", password=loginpw, authentication=NTLM)

    if not c.bind():
        return jsonify({"message": f"Failed to bind: {c.result['message']}"}), 500

    # Create user
    try:
        c.add(
            userdn,
            attributes={
                "cn": username,
                "givenName": username,
                "sn": "User",
                "displayName": username,
                "userPrincipalName": f"{username}@test.local",
                "sAMAccountName": username,
                "userPassword": userpswd,  # Replace with desired password
                "objectClass": ["top", "person", "organizationalPerson", "user"],
            },
        )

        # Set password
        c.extend.microsoft.modify_password(userdn, userpswd)

        # Enable user
        c.modify(userdn, {"userAccountControl": [("MODIFY_REPLACE", 512)]})

        # Enable user
        c.modify(userdn, {"userAccountControl": [("MODIFY_REPLACE", 64)]})

        # Set dial-in network access permission to allow access
        c.modify(userdn, {"msNPAllowDialin": [("MODIFY_REPLACE", [True])]})

        # Add the user to the group
        c.modify(group_dn, {"member": [("MODIFY_ADD", [userdn])]})

        # Check result
        if c.result["result"] == 0:
            return jsonify({"message": f"User '{userdn}' successfully added."}), 200
        else:
            return (
                jsonify(
                    {
                        "message": f"Failed to add user '{userdn}'. Error: {c.result['message']}"
                    }
                ),
                500,
            )

    except Exception as e:
        return jsonify({"message": f"Failed to add user: {str(e)}"}), 500
    finally:
        c.unbind()


if __name__ == "__main__":
    app.run(debug=True)
