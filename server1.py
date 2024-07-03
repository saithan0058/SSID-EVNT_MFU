from flask import (
    Flask,
    logging,
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
import io
import random
from pymongo import MongoClient
import os
import csv
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, NTLM,SUBTREE,MODIFY_ADD


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

@app.route('/testtest', methods=['GET'])
def testtest():
    return send_from_directory('.', 'testtest.html')

# testcsv file template
@app.route('/adduserpage', methods=['GET'])
def adduserpage():
    return send_from_directory('.', 'pagetestcsv.html')




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

    try:
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
        users = []
        with open(csv_filename, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 4:  # Assuming the CSV has 4 columns: ID card number, name, phone number, email
                    user = {
                        "ssid_id": ssid_id,
                        "id_card_number": row[0],
                        "name": row[1],
                        "phone_number": row[2],
                        "email": row[3],
                    }
                    users.append(user)

        # Insert all users into the MongoDB collection
        if users:
            history_collection.insert_many(users)
            logging.info(f"Inserted users: {users}")
        else:
            logging.info("No users found in CSV file.")

        device = {
            "device_type": "cisco_ios",
            "ip": "172.30.99.56",
            "username": "admin",
            "password": "CITS@WLC2023",
            "secret": "CITS@WLC2023",
        }

        # Connect to the Cisco device
        net_connect = ConnectHandler(**device)
        net_connect.enable()

        # Send the command
        output = net_connect.send_command("show wlan summary")
        logging.info(output)

        wlan_ids = []
        lines = output.splitlines()
        for line in lines[5:]:
            if line.strip():
                match = re.match(r"^\s*(\d+)", line)
                if match:
                    wlan_id = match.group(1)
                    wlan_ids.append(wlan_id)

        # Print the WLAN IDs
        for wlan_id in wlan_ids:
            logging.info(wlan_id)

        existing_array = [None] * 15

        # Add the values from wlan_ids to the existing array
        for i in range(len(wlan_ids)):
            existing_array[i] = wlan_ids[i]

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
            "no security ft adaptive",
            "security dot1x authentication-list list",
            "security ft",
            "security wpa akm ft dot1x",
            "no shutdown",
            "exit",
            f"wireless tag policy {location2}",
            f"wlan {ssid2} policy MFUPolicyProfile1",
            "end",
        ]

        output = net_connect.send_config_set(config_commands)
        logging.info(output)

        # Disconnect from the Cisco device
        net_connect.disconnect()

    except Exception as e:
        logging.error(f"An error occurred: {e}")

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

@app.route('/delete_ssid/<ssid_id>', methods=['DELETE'])
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
    
# server prop----------------------------------------------------------------------------------------------------
server_address = "ldaps://10.1.55.210:636"
domain = "test"
loginun = "Administrator"
loginpw = "12345678Xx"
# server prop----------------------------------------------------------------------------------------------------

# add user in ad ----------------------------------------------------------------------------------------------------

@app.route("/add_user", methods=["POST"]) #เพิ่มรายชื่อทีละคน
def add_user():
    username = request.json.get("username")
    useremail = request.json.get("useremail")
    userpswd = request.json.get("userpswd")
    userdn = request.json.get("userdn")
    group_dn = request.json.get("group_dn")

    # Connect to LDAP server
    s = Server(server_address, connect_timeout=5, use_ssl=True, get_info=ALL)
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
# add user in ad ----------------------------------------------------------------------------------------------------

# add user in ad ----------------------------------------------------------------------------------------------------
group_dn = "CN=testgroup1,OU=guest1,OU=Guest,DC=test,DC=local" #csv file add
@app.route("/add_usercsv/<GroupandOU>", methods=["POST"])
def add_usercsv(GroupandOU):
    group_dn = f'CN={GroupandOU},OU={GroupandOU},OU=Guest,DC=test,DC=local'
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Invalid file format"}), 400

    # Connect to the AD server
    server = Server(server_address, connect_timeout=5, use_ssl=True, get_info=ALL)
    conn = Connection(
        server, user=f"{domain}\\{loginun}", password=loginpw, authentication=NTLM
    )

    if not conn.bind():
        return jsonify({"error": f"Failed to connect to AD server. Error: {conn.result}"}), 500

    # Read users from CSV and process them
    try:
        # เปิดไฟล์ในโหมดข้อความ
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.DictReader(stream)
        results = []
        for row in reader:
            username = row["username"]
            userpswd = row["password"]
            cn = row["cn"]
            givenName = row["givenName"]
            sn = row["sn"]
            displayName = row["username"]
            userPrincipalName = row["username"]
            sAMAccountName = row["username"]
            userdn = f"CN={cn},OU={GroupandOU},OU=Guest,DC=test,DC=local"

            # สร้างผู้ใช้
            conn.add(
                userdn,
                attributes={
                    "cn": cn,
                    "givenName": givenName,
                    "sn": sn,
                    "displayName": displayName,
                    "userPrincipalName": userPrincipalName,
                    "sAMAccountName": sAMAccountName,
                    "userPassword": userpswd,
                    "objectClass": ["top", "person", "organizationalPerson", "user"],
                },
            )

            # ตั้งรหัสผ่าน - ต้องทำก่อนเปิดใช้งานผู้ใช้
            conn.extend.microsoft.modify_password(userdn, userpswd)

            # เปิดใช้งานผู้ใช้ (หลังจากตั้งรหัสผ่าน)
            conn.modify(userdn, {"userAccountControl": [(MODIFY_REPLACE, 512)]})

            # อนุญาตการเข้าถึงเครือข่าย dial-in
            conn.modify(userdn, {"msNPAllowDialin": [(MODIFY_REPLACE, [True])]})

            # เพิ่มผู้ใช้ในกลุ่ม
            conn.modify(group_dn, {"member": [(MODIFY_ADD, [userdn])]})

            # ตรวจสอบผลลัพธ์
            if conn.result["result"] == 0:
                results.append({"username": username, "status": "success"})
            else:
                results.append({"username": username, "status": "failure", "error": conn.result["message"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # ปิดการเชื่อมต่อ
        conn.unbind()

    return jsonify(results), 200

# add user in ad ----------------------------------------------------------------------------------------------------


# get user in ad ----------------------------------------------------------------------------------------------------

@app.route('/get_users/<base_dn>', methods=['GET']) #get user list เช็ครายชื่อในouนั้นๆ
def get_users(base_dn):
    try:
        # Connect to LDAP server
        server = Server(server_address, connect_timeout=5, use_ssl=True, get_info=ALL)
        conn = Connection(server, user=f"{domain}\\{loginun}", password=loginpw, authentication=NTLM, auto_bind=True)
        
        # Define the base DN based on the provided OU name
        base_dn = f"OU={base_dn},OU=Guest,DC=test,DC=local"

        # Search for all users in the specified nested OU and retrieve their common names (cn)
        conn.search(
            search_base=base_dn,
            search_filter='(objectClass=person)',  # Filter for user objects
            search_scope=SUBTREE,
            attributes=['cn']  # Retrieve only the common name attribute
        )
        
        # Store user names in a list
        user_names = [entry.cn.value for entry in conn.entries]
        
        # Unbind the connection
        conn.unbind()
        
        # Return user names as JSON response
        return jsonify({'users': user_names})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# get user in ad ----------------------------------------------------------------------------------------------------

# delete user in ad ---------------------------------------------------------------------------------------------------- 
@app.route('/delete_users/<oudn>', methods=['DELETE'])
def delete_users(oudn):
    try:
        # Connect to the LDAP server
        server = Server(server_address, connect_timeout=5, use_ssl=True, get_info=ALL)
        conn = Connection(server, user=f"{domain}\\{loginun}", password=loginpw, authentication=NTLM, auto_bind=True)

        # Define the base DN based on the provided OU name
        base_dn = f"OU={oudn},OU=Guest,DC=test,DC=local"

        # Search for all users in the specified OU
        conn.search(
            search_base=base_dn,
            search_filter="(objectClass=user)",
            search_scope=SUBTREE,
            attributes=["distinguishedName"],
        )

        # Iterate through the search results and delete each user
        messages = []
        for entry in conn.entries:
            user_dn = entry.distinguishedName.value
            conn.delete(user_dn)
            if conn.result["result"] == 0:
                messages.append(f"User '{user_dn}' successfully deleted.")
                print(f"User '{user_dn}' successfully deleted.")
            else:
                messages.append(f"Failed to delete user '{user_dn}'. Error: {conn.result['message']}")
                print(f"Failed to delete user '{user_dn}'. Error: {conn.result['message']}")

        # Unbind the LDAP connection
        conn.unbind()

        return jsonify({'message': messages})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
# delete user in ad ---------------------------------------------------------------------------------------------------- 

# Serve static files from the 'static' folder
@app.route("/static/<path:filename>", methods=["GET"])
def serve_static(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, "static"), filename)


if __name__ == "__main__":
    app.run(host="localhost", port=3000)





