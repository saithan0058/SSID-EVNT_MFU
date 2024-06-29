import csv
import ldap3
import random
# Set the LDAP server details
ldap_server = 'ldap://192.168.234.129'
ldap_admin_username = 'cn=admin,dc=example,dc=com'
ldap_admin_password = '123'
ldap_base_dn = 'ou=people,dc=example,dc=com'

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
server = ldap3.Server(ldap_server)
conn = ldap3.Connection(server, user=ldap_admin_username, password=ldap_admin_password)
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
    server = ldap3.Server(ldap_server)
    conn = ldap3.Connection(server, user=ldap_admin_username, password=ldap_admin_password)
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
            'uidNumber': random_num,
            'gidNumber': 10002,
            'homeDirectory': "/home/user",
            'loginShell': "/bin/bash",
            'userPassword': row['password']
        }
        
        # Create the new user entry in the LDAP server
        user_dn = f'cn={row["cn"]},{ldap_base_dn}'
        conn.add(user_dn, object_classes, user_attributes)

# Unbind from the LDAP server
conn.unbind()
