import ldap3

import random
# Set the LDAP server details
ldap_server = 'ldap://192.168.234.129'
ldap_admin_username = 'cn=admin,dc=example,dc=com'
ldap_admin_password = '123'
ldap_base_dn = 'ou=people,dc=example,dc=com'

# Create a connection to the LDAP server and bind as the admin user
server = ldap3.Server(ldap_server)
conn = ldap3.Connection(server, user=ldap_admin_username, password=ldap_admin_password)
conn.bind()

# Search for entries and retrieve only the uidNumber attribute
conn.search(ldap_base_dn, '(objectClass=*)', attributes=['uidNumber'])
entries = conn.entries

# Extract the uidNumber values from the LDAP entries
uid_numbers = [entry.uidNumber.value for entry in entries if 'uidNumber' in entry]

# Print the uidNumber values
for uid_number in uid_numbers:
    print(uid_number)

# Unbind from the LDAP server
conn.unbind()
# Assuming you have retrieved the LDAP entries and stored them in a list called 'entries'
uid_numbers = []

# Extract uidNumber from the LDAP entries and add them to uid_numbers list
for entry in entries:
    uid_number = entry.uidNumber.value
    uid_numbers.append(uid_number)

existing_array = [None] * 100

# Add the values from uid_numbers to the existing array
for i in range(len(uid_numbers)):
    existing_array[i] = uid_numbers[i]

# Print the updated array
print(existing_array)

next_position = existing_array.index(None)

# Generate a random number between 1 and 16
random_num = random.randint(10000, 12000)

# Check if the random number already exists in the array
while str(random_num) in existing_array:
    random_num = random.randint(10000, 12000)  # Generate a new random number

# Replace the next available position with the random number
existing_array[next_position] = str(random_num)

print(existing_array)  # Print the updated array