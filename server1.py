from flask import (
    Flask,
    logging,
    request,
    send_from_directory,
    render_template,
    redirect,
    session,
    url_for,
    jsonify,
)
import datetime
from netmiko import ConnectHandler
import re
import io
import random
import logging
from pymongo import MongoClient
import os
import csv
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, NTLM, SUBTREE, MODIFY_ADD


current_time = datetime.datetime.now()
logging.basicConfig(level=logging.DEBUG)  # เพิ่มการตั้งค่าการล็อกเพื่อดูข้อผิดพลาด

# ปรับเปลี่ยนเป็นพุทธศักราช
buddhist_year = current_time.year + 543

# สร้างวัตถุ datetime ใหม่ที่มีการเปลี่ยนแปลงแล้ว
buddhist_time = current_time.replace(year=buddhist_year)
# แสดงวันที่แบบพุทธศักราช
formatted_time = buddhist_time.strftime("%Y-%m-%d %H:%M:%S")


app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set a secret key for session management

# Mock database or user credentials (for demonstration)
USER_CREDENTIALS = [{"username": "admin", "password": "admin"}]
USER_CREDENTIALS.append({"username": "jame", "password": "jame"})
USER_CREDENTIALS.append({"username": "pure", "password": "pure"})


# Middleware to prevent caching of restricted pages after logout
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    return response


# Routes


@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("homepage"))  # Redirect logged-in user to homepage
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Check if username and password match the stored credentials
    user = next(
        (
            u
            for u in USER_CREDENTIALS
            if u["username"] == username and u["password"] == password
        ),
        None,
    )
    if user:
        session["username"] = username
        return redirect(url_for("homepage"))
    else:
        return render_template("login.html", error="Invalid username or password")


@app.route("/logout")
def logout():
    # Clear the session
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/homepage")
def homepage():
    if "username" in session:
        return render_template("history.html", username=session["username"])

    else:
        return redirect(url_for("index"))  # Redirect to login if not logged in


@app.route("/nopassword")
def nopassword():
    if "username" in session:
        return render_template("nopassword.html", username=session["username"])
    else:
        return redirect(url_for("index"))  # Redirect to login if not logged in


@app.route("/psk")
def psk():
    if "username" in session:
        return render_template("psk.html", username=session["username"])
    else:
        return redirect(url_for("index"))  # Redirect to login if not logged in


@app.route("/individual")
def individual():
    if "username" in session:
        return render_template("Individual.html", username=session["username"])
    else:
        return redirect(url_for("index"))  # Redirect to login if not logged in


# if __name__ == "__main__":
#     app.run(host="localhost", port=3000)
# @app.route("/", methods=["GET"])
# def index():
#     with open("tester.html", "r", encoding="utf-8") as file:
#         return file.read()


@app.route("/testtest", methods=["GET"])
def testtest():
    return send_from_directory(".", "testtest.html")


# testcsv file template
@app.route("/adduserpage", methods=["GET"])
def adduserpage():
    return send_from_directory(".", "pagetestcsv.html")


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
    try:
        ssid = request.form["ssid"]
        password = request.form["password"]
        event = request.form["event"]
        location = request.form["location"]
        logging.debug(f"Received data - SSID: {ssid}, Event: {event}, Location: {location}")

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
        logging.debug("Connected to Cisco device")

        # Retrieve WLAN summary
        output = net_connect.send_command("show wlan summary")
        logging.debug(f"WLAN summary output: {output}")

        # Extract WLAN IDs
        wlan_ids = []
        lines = output.splitlines()
        for line in lines[5:]:
            if line.strip():
                match = re.match(r"^\s*(\d+)", line)
                if match:
                    wlan_id = match.group(1)
                    wlan_ids.append(wlan_id)
        logging.debug(f"Extracted WLAN IDs: {wlan_ids}")

        # Initialize array for existing WLAN IDs
        existing_array = [None] * 15
        for i in range(len(wlan_ids)):
            existing_array[i] = wlan_ids[i]

        # Find the next available position
        next_position = existing_array.index(None)

        # Generate a unique random WLAN ID
        random_num = random.randint(1, 16)
        while str(random_num) in existing_array:
            random_num = random.randint(1, 16)

        # Replace the next available position with the new WLAN ID
        existing_array[next_position] = str(random_num)

        # Configuration commands for the new SSID
        config_commands = [
            f"wlan {ssid} {random_num} {ssid}",
            "security ft",
            f"security wpa psk set-key ascii 0 {password} {password}",
            "no security wpa akm dot1x",
            "security wpa akm psk",
            "security wpa akm ft psk",
            "no shutdown",
            "exit",
            f"wireless tag policy {location}",
            f"wlan {ssid} policy MFUPolicyProfile1",
            "end",
        ]

        # Send configuration commands to the Cisco device
        output = net_connect.send_config_set(config_commands)
        logging.debug(f"Configuration output: {output}")

        # Disconnect from the Cisco device
        net_connect.disconnect()
        logging.debug("Disconnected from Cisco device")

        return redirect(url_for("history"))

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return "Internal Server Error", 500

@app.route('/handle_data', methods=['POST'])
def handle_data():
    # Extract the JSON data from the request
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Unsupported Media Type'}), 415
    
    # Extract specific parts of the data
    ssid2 = data.get('ssid2')
    event2 = data.get('event2')
    location2 = data.get('location2')
    ouGroup = data.get('ouGroup')
    users = data.get('users', [])
    
    # Process the data as needed (e.g., print or log it)
    print(f'SSID2: {ssid2}')
    print(f'Event2: {event2}')
    print(f'Location2: {location2}')
    print(f'OU Group: {ouGroup}')
    
    for user in users:
        index = user.get('index')
        idcard = user.get('idcard')
        name = user.get('name')
        phone = user.get('phone')
        email = user.get('email')
        print(f'User {index}: ID Card: {idcard}, Name: {name}, Phone: {phone}, Email: {email}')
    
    # Return a JSON response
    return jsonify({'status': 'success', 'data_received': data}), 200

@app.route('/configure_ssid2', methods=['POST']) #AAA
def configure_ssid2():
    data = request.get_json()

    # Extract specific parts of the data
    ssid2 = data.get('ssid2')
    event2 = data.get('event2')
    location2 = data.get('location2')
    ouGroup = data.get('ouGroup')
    users = data.get('users', [])
    dateRange = data.get('dateRange')  # ดึงค่าวันที่จากคำขอ

    # Optional: จัดการกับค่าวันที่ ถ้าจำเป็น
    if dateRange:
        start_date, end_date = dateRange.split(' - ')
        print(f"Start Date: {start_date}, End Date: {end_date}")

    post(ssid2, event2, location2, ouGroup, users)

    device = {
        'device_type': 'cisco_ios',
        'ip': '172.30.99.56',
        'username': 'admin',
        'password': 'CITS@WLC2023',
        'secret': 'CITS@WLC2023',
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
            match = re.match(r'^\s*(\d+)', line)
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
        f'wlan {ssid2} {random_num} {ssid2}',
        'no security ft adaptive',
        'security dot1x authentication-list list',
        'security ft',
        'security wpa akm ft dot1x',
        'no shutdown',
        'exit',
        f'wireless tag policy {location2}',
        f'wlan {ssid2} policy MFUPolicyProfile1',
        'end',
    ]

    output = net_connect.send_config_set(config_commands)
    print(output)

    # Disconnect from the Cisco device
    net_connect.disconnect()

    return redirect(url_for('history'))




def post(ssid, event, location):
    
    current_time = datetime.datetime.now()

# ปรับเปลี่ยนเป็นพุธศักราช
    buddhist_year = current_time.year + 543

# สร้างวัตถุ datetime ใหม่ที่มีการเปลี่ยนแปลงแล้ว
    buddhist_time = current_time.replace(year=buddhist_year)
# แสดงวันที่แบบพุธศักราช
    formatted_time = buddhist_time.strftime("%Y-%m-%d %H:%M:%S")    
    # Connect to the MongoDB server
    client = MongoClient('mongodb://localhost:27017')

    # Access the database
    db = client['mydb']

    # Access the collection
    collection = db['ssid']

    # Create a document to insert
    document = {
        'ssid': ssid,
        'event': event,
        'location': location,              
        'time': formatted_time,
        
    }

    # Insert the document into the collection
    collection.insert_one(document)

    # Close the MongoDB connection
    client.close()

def post(ssid1, event1, location1):
    
    
    current_time = datetime.datetime.now()

# ปรับเปลี่ยนเป็นพุธศักราช
    buddhist_year = current_time.year + 543

# สร้างวัตถุ datetime ใหม่ที่มีการเปลี่ยนแปลงแล้ว
    buddhist_time = current_time.replace(year=buddhist_year)
# แสดงวันที่แบบพุธศักราช
    formatted_time = buddhist_time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Connect to the MongoDB server
    client = MongoClient('mongodb://localhost:27017')

    # Access the database
    db = client['mydb']

    # Access the collection
    collection = db['ssid']

    # Create a document to insert
    document = {
        'ssid' : ssid1,
        'event': event1,
        'location': location1,         
        'time': formatted_time
    }

    # Insert the document into the collection
    collection.insert_one(document)

    # Close the MongoDB connection
    client.close()

def post(ssid2, event2, location2, ouGroup, users):
    
    
    current_time = datetime.datetime.now()

# ปรับเปลี่ยนเป็นพุธศักราช
    buddhist_year = current_time.year + 543

# สร้างวัตถุ datetime ใหม่ที่มีการเปลี่ยนแปลงแล้ว
    buddhist_time = current_time.replace(year=buddhist_year)
# แสดงวันที่แบบพุธศักราช
    formatted_time = buddhist_time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Connect to the MongoDB server
    client = MongoClient('mongodb://localhost:27017')

    # Access the database
    db = client['mydb']

    # Access the collection
    collection = db['ssid']

    # Create a document to insert
    document = {
        'ssid' : ssid2,
        'event': event2,
        'location': location2,          
        'time': formatted_time,
        'ouGroup':ouGroup,
        'users':users,

    }

    # Insert the document into the collection
    collection.insert_one(document)

    # Close the MongoDB connection
    client.close()

@app.route("/update_user", methods=["POST"])
def update_user():
    data = request.get_json()
    id_card = data.get("idcard")
    name = data.get("name")
    phone = data.get("phone")
    email = data.get("email")

    client = MongoClient("mongodb://localhost:27017")
    db = client["mydb"]
    collection = db["history"]

    result = collection.update_one(
        {"id_card_number": id_card},
        {"$set": {"name": name, "phone_number": phone, "email": email}}
    )

    if result.modified_count > 0:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "failed"}), 400

@app.route("/delete_user/<id_card>", methods=["DELETE"])
def delete_user(id_card):
    client = MongoClient("mongodb://localhost:27017")
    db = client["mydb"]
    collection = db["history"]

    result = collection.delete_one({"id_card_number": id_card})

    if result.deleted_count > 0:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "failed"}), 400



@app.route("/delete_ssid/<ssid_id>", methods=["DELETE"])
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


@app.route("/add_user", methods=["POST"])  # เพิ่มรายชื่อทีละคน
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
group_dn = "CN=testgroup1,OU=guest1,OU=Guest,DC=test,DC=local"  # csv file add


@app.route("/add_usercsv/<GroupandOU>", methods=["POST"])
def add_usercsv(GroupandOU):
    group_dn = f"CN={GroupandOU},OU={GroupandOU},OU=Guest,DC=test,DC=local"
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if not file.filename.endswith(".csv"):
        return jsonify({"error": "Invalid file format"}), 400

    # Connect to the AD server
    server = Server(server_address, connect_timeout=5, use_ssl=True, get_info=ALL)
    conn = Connection(
        server, user=f"{domain}\\{loginun}", password=loginpw, authentication=NTLM
    )

    if not conn.bind():
        return (
            jsonify({"error": f"Failed to connect to AD server. Error: {conn.result}"}),
            500,
        )

    # Read users from CSV and process them
    try:
        # เปิดไฟล์ในโหมดข้อความ
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.DictReader(stream)
        results = []
        for row in reader:
            username = row["username"]
            userpswd = row["phone_number"]
            cn = row["username"]
            sn = row["username"]
            givenName = row["username"]
            displayName = row["username"]
            userPrincipalName = row["ID_crad"]
            sAMAccountName = row["ID_crad"]
            userdn = f"CN={cn},OU={GroupandOU},OU=Guest,DC=test,DC=local"

            # สร้างผู้ใช้
            conn.add(
                userdn,
                attributes={
                    "cn": cn,
                    "givenName": givenName,
                    "sn": sn,
                    "displayName": displayName,
                    "userPrincipalName": f"{userPrincipalName}@test.local",
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
                results.append(
                    {
                        "username": username,
                        "status": "failure",
                        "error": conn.result["message"],
                    }
                )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # ปิดการเชื่อมต่อ
        conn.unbind()

    return jsonify(results), 200


# add user in ad ----------------------------------------------------------------------------------------------------

# add user json in ad ----------------------------------------------------------------------------------------------------
@app.route("/add_userjson/<GroupandOU>", methods=["POST"])  # Add multiple users
def add_users(GroupandOU):
    group_dn = f"CN={GroupandOU},OU={GroupandOU},OU=Guest,DC=test,DC=local"
    try:
        users = request.get_json()
        if not isinstance(users, list):
            return jsonify({"error": "JSON data must be a list of user objects"}), 400
        
        results = []
        for user in users:
            username = user.get("name")
            userpswd = user.get("phone")
            userPrincipalName = user.get("idcard")
            sAMAccountName = user.get("idcard")
            userdn = f"CN={username},OU={GroupandOU},OU=Guest,DC=test,DC=local"

            # Connect to LDAP server
            s = Server(server_address, connect_timeout=5, use_ssl=True, get_info=ALL)
            c = Connection(s, user="test\\Administrator", password=loginpw, authentication=NTLM)

            if not c.bind():
                results.append({"username": username, "status": "failure", "message": f"Failed to bind: {c.result['message']}"})
                continue  # Skip to next user if binding fails

            try:
                # Create user
                c.add(
                    userdn,
                    attributes={
                        "cn": username,
                        "givenName": username,
                        "sn": username,
                        "displayName": username,
                        "userPrincipalName": f"{userPrincipalName}@test.local",
                        "sAMAccountName": sAMAccountName,
                        "userPassword": userpswd,  # Replace with desired password
                        "objectClass": ["top", "person", "organizationalPerson", "user"],
                    },
                )

                # Set password
                c.extend.microsoft.modify_password(userdn, userpswd)

                # Enable user
                c.modify(userdn, {"userAccountControl": [("MODIFY_REPLACE", 512)]})

                # Set dial-in network access permission to allow access
                c.modify(userdn, {"msNPAllowDialin": [("MODIFY_REPLACE", [True])]})

                # Add the user to the group
                c.modify(group_dn, {"member": [("MODIFY_ADD", [userdn])]})

                # Check result
                if c.result["result"] == 0:
                    results.append({"username": username, "status": "success"})
                else:
                    results.append({"username": username, "status": "failure", "message": f"Failed to add user '{userdn}'. Error: {c.result['message']}"})
            
            except Exception as e:
                results.append({"username": username, "status": "failure", "message": f"Failed to add user: {str(e)}"})
            
            finally:
                c.unbind()

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": f"Failed to process request: {str(e)}"}), 500

# add user json in ad ----------------------------------------------------------------------------------------------------


# get ous without users  in ad ----------------------------------------------------------------------------------------------------
base_dn = f"dc={domain},dc=local"
guest_dn = f"ou=Guest,{base_dn}"
# Function to retrieve all OUs within the Guest OU
def get_ous_in_guest(conn):
    try:
        conn.search(guest_dn, '(objectClass=organizationalUnit)', attributes=['ou'])
        return [entry.entry_dn for entry in conn.entries]
    except Exception as e:
        raise Exception(f"Error retrieving OUs in Guest: {str(e)}")

# Function to check if an OU has users
def has_users(conn, ou_dn):
    try:
        conn.search(ou_dn, '(objectClass=person)', search_scope=SUBTREE)
        return len(conn.entries) > 0
    except Exception as e:
        raise Exception(f"Error checking users in OU {ou_dn}: {str(e)}")

@app.route("/getOUcheck", methods=["GET"])
def get_ou_check():
    try:
        server = Server(server_address, connect_timeout=5, use_ssl=True, get_info=ALL)
        conn = Connection(
            server,
            user=f"{domain}\\{loginun}",
            password=loginpw,
            authentication=NTLM,
            auto_bind=True,
        )

        # Retrieve all OUs within the Guest OU
        ous_in_guest = get_ous_in_guest(conn)

        # Find OUs within Guest that do not have users
        ous_without_users = [ou.split(",")[0].split("=")[1] for ou in ous_in_guest if not has_users(conn, ou)]

        # Close LDAP connection
        conn.unbind()

        # Return JSON response
        return jsonify(ous_without_users)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# get ous without users  in ad ----------------------------------------------------------------------------------------------------

# get user in ad ----------------------------------------------------------------------------------------------------
@app.route("/get_users/<base_dn>", methods=["GET"])  # get user list เช็ครายชื่อในouนั้นๆ
def get_users(base_dn):
    try:
        # Connect to LDAP server
        server = Server(server_address, connect_timeout=5, use_ssl=True, get_info=ALL)
        conn = Connection(
            server,
            user=f"{domain}\\{loginun}",
            password=loginpw,
            authentication=NTLM,
            auto_bind=True,
        )

        # Define the base DN based on the provided OU name
        base_dn = f"OU={base_dn},OU=Guest,DC=test,DC=local"

        # Search for all users in the specified nested OU and retrieve their common names (cn)
        conn.search(
            search_base=base_dn,
            search_filter="(objectClass=person)",  # Filter for user objects
            search_scope=SUBTREE,
            attributes=["cn"],  # Retrieve only the common name attribute
        )

        # Store user names in a list
        user_names = [entry.cn.value for entry in conn.entries]

        # Unbind the connection
        conn.unbind()

        # Return user names as JSON response
        return jsonify({"users": user_names})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# get user in ad ----------------------------------------------------------------------------------------------------


# delete user in ad ----------------------------------------------------------------------------------------------------
@app.route("/delete_users/<oudn>", methods=["DELETE"])
def delete_users(oudn):
    try:
        # Connect to the LDAP server
        server = Server(server_address, connect_timeout=5, use_ssl=True, get_info=ALL)
        conn = Connection(
            server,
            user=f"{domain}\\{loginun}",
            password=loginpw,
            authentication=NTLM,
            auto_bind=True,
        )

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
                messages.append(
                    f"Failed to delete user '{user_dn}'. Error: {conn.result['message']}"
                )
                print(
                    f"Failed to delete user '{user_dn}'. Error: {conn.result['message']}"
                )

        # Unbind the LDAP connection
        conn.unbind()

        return jsonify({"message": messages})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# delete user in ad ----------------------------------------------------------------------------------------------------

# add in db ----------------------------------------------------------------------------------------------------
@app.route("/adduser_mongo", methods=["POST"])
def add_user_mongo():
    try:
        # Parse request data
        data = request.json
        
        # Validate required fields
        required_fields = ["id","namessid", "evenname", "location", "starttime", "endtime", "users"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400
        
        # Convert starttime and endtime to datetime objects
        # starttime = datetime.fromisoformat(data["starttime"])
        # endtime = datetime.fromisoformat(data["endtime"])

        # Construct the document
        document = {
            "id": data["id"],
            "namessid": data["namessid"],
            "evenname": data["evenname"],
            "location": data["location"],
            "starttime": data["starttime"],
            "endtime": data["endtime"],
            "users": data["users"]
        }

        # Insert the document into the collection
        result = collection.insert_one(document)
        
        # Return success response
        return jsonify({"message": "Document inserted successfully", "inserted_id": str(result.inserted_id)}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# add in db ----------------------------------------------------------------------------------------------------

# get data in db ----------------------------------------------------------------------------------------------------
from bson.json_util import dumps
@app.route("/getusers_mongo", methods=["GET"])
def get_users_mongo():
    try:
        # Retrieve all documents from the collection
        documents = collection.find()

        # Convert documents to a JSON string
        documents_list = list(documents)
        json_docs = dumps(documents_list)

        # Return JSON response
        return json_docs, 200, {'Content-Type': 'application/json'}
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# get data in db ----------------------------------------------------------------------------------------------------

# Serve static files from the 'static' folder
@app.route("/static/<path:filename>", methods=["GET"])
def serve_static(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, "static"), filename)


if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)
