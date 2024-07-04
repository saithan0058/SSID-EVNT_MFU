import csv
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, MODIFY_ADD, NTLM

# Define AD connection parameters
domain = "test"
loginun = "Administrator"
loginpw = "12345678Xx"
server_address = "ldaps://10.1.55.210:636"
group_dn = "CN=guest1,OU=guest1,OU=Guest,DC=test,DC=local"

# Connect to the AD server
server = Server(server_address, connect_timeout=5, use_ssl=True, get_info=ALL)
conn = Connection(
    server, user=f"{domain}\\{loginun}", password=loginpw, authentication=NTLM
)

if not conn.bind():
    print(f"Failed to connect to AD server. Error: {conn.result}")
    exit(1)

# Read users from CSV and process them
with open("user100.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        username = row["username"]
        userpswd = row["phone_number"]
        cn = row["username"]
        sn = row["username"]
        givenName = row["username"]
        displayName = row["username"]
        userPrincipalName = row["ID_crad"]
        sAMAccountName = row["ID_crad"]
        userdn = f"CN={cn},OU=guest1,OU=Guest,DC=test,DC=local"

        # Create user
        conn.add(
            userdn,
            attributes={
                "cn": cn,
                "sn":sn,
                "givenName": givenName,
                "displayName": displayName,
                "userPrincipalName": f"{userPrincipalName}@test.local",
                "sAMAccountName": sAMAccountName,
                "userPassword": userpswd,
                "objectClass": ["top", "person", "organizationalPerson", "user"],
            },
        )

        # Set password - must be done before enabling user
        conn.extend.microsoft.modify_password(userdn, userpswd)

        # Enable user (after password set)
        conn.modify(userdn, {"userAccountControl": [(MODIFY_REPLACE, 512)]})

        # Set dial-in network access permission to allow access
        conn.modify(userdn, {"msNPAllowDialin": [(MODIFY_REPLACE, [True])]})

        # Add the user to the group
        conn.modify(group_dn, {"member": [(MODIFY_ADD, [userdn])]})

        # Check result
        if conn.result["result"] == 0:
            print(f"User '{username}' successfully added.")
        else:
            print(f"Failed to add user '{username}'. Error: {conn.result['message']}")

# Unbind the connection
conn.unbind()
