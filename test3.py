import csv
import random
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, NTLM
# Set the LDAP server details
ldap_server = 'ldaps://10.1.55.210:636'
ldap_admin_username = 'test\\Administrator'
ldap_admin_password = '12345678Xx'
UOunder = 'guest1'
ldap_base_dn = f'OU={UOunder},OU=Guest,DC=test,DC=local'

# Set the path to the CSV file
csv_file_path = 'Book1.csv'

# Define the LDAP object classes for a new user
object_classes = [
    'top',
    'posixAccount',
    'inetOrgPerson',
    'organizationalPerson',
    'person'
]

# Create a connection to the LDAP server and bind as the admin user
server = Server(ldap_server, connect_timeout=5, use_ssl=True, get_info=ALL)
conn = Connection(server, user=ldap_admin_username, password=ldap_admin_password, authentication=NTLM)
conn.bind()

# Read user information from the CSV file and create user entries in the LDAP server
with open(csv_file_path, 'r') as file:
    
    object_classes = [
        'top',
        'posixAccount',
        'inetOrgPerson',
        'organizationalPerson',
        'person'
    ]
    server = Server(ldap_server)
    conn = Connection(server, user=ldap_admin_username, password=ldap_admin_password)
    conn.bind()
    conn.search(ldap_base_dn, '(objectClass=*)', attributes=['uidNumber'])
    entries = conn.entries
    
    uid_numbers = [entry.uidNumber.value for entry in entries if 'uidNumber' in entry]
    
    for uid_number in uid_numbers:
        print(uid_number)
    
    uid_numbers = []
    
    for entry in entries:
        uid_number = entry.uidNumber.value
        uid_numbers.append(uid_number)

    existing_array = [None] * 100
    
    for i in range(len(uid_numbers)):
        existing_array[i] = uid_numbers[i]
    
    print(existing_array)

    next_position = existing_array.index(None)
    random_num = random.randint(10000, 12000)

# Check if the random number already exists in the array
    while str(random_num) in existing_array:
        random_num = random.randint(10000, 12000)  # Generate a new random number
    print(random_num)
    
    reader = csv.DictReader(file)
    
    
    for row in reader:
        
        random_num = random.randint(10000, 12000)
        # Set the user attributes based on the CSV row data
        user_attributes = {
            'cn': row['cn'],
            'givenName': row['givenName'],
            'sn': row['sn'],
            'uid': row['username'],
            'sAMAccountName': row['username'],
            'displayName': row['username'],
            'uidNumber': random_num,
            'gidNumber': 10002,
            'loginShell': "/bin/bash",
            'userPassword': row['password'],
            'userPrincipalName': f'{row['cn']}@test.local'
            
        }
        
        # Create the new user entry in the LDAP server
        user_dn = f'cn={row["cn"]},{ldap_base_dn}'
        group_dn = 'CN=WIFI USERS,CN=Users,DC=test,DC=local'
        conn.add(user_dn, object_classes, user_attributes)

        # set password - must be done before enabling user
        # you must connect with SSL to set the password 
        conn.extend.microsoft.modify_password(user_dn, row['password'])
        
        # enable user (after password set)
        conn.modify(user_dn, {'userAccountControl': [('MODIFY_REPLACE', 512)]})
        
        # ena user
        conn.modify(user_dn, {'userAccountControl': [('MODIFY_REPLACE', 64)]})   
        
        # set dail-in network access permission to allow access
        conn.modify(user_dn, {'msNPAllowDialin': [('MODIFY_REPLACE', [True])]})
        # Add the user to the group
        conn.modify(group_dn, {'member': [('MODIFY_ADD', [user_dn])]})
         
         # C heck result
        if conn.result['result'] == 0:
            print(f"User '{user_dn}' successfully added.")
        else:
            print(f"Failed to add user '{user_dn}'. Error: {conn.result['message']}")
# Unbind from the LDAP server
conn.unbind()
