from ldap3 import Server, Connection, ALL, MODIFY_REPLACE

# Define server connection details
server = Server('ldaps://10.1.55.210:636', use_ssl=True, get_info=ALL)  # Replace with your Active Directory server IP or hostname

# Establish connection
con = Connection(server, user='test\\Administrator', password='12345678Xx', auto_bind=True)

# Define new user details
new_user_dn = 'CN=jame,OU=Guest,DC=test,DC=local'
new_user_attributes = {
    'cn': 'jame',
    'givenName': 'jame',
    'sn': 'User',
    'displayName': 'james',
    'userPrincipalName': 'james@test.local',
    'sAMAccountName': 'james',
    'userPassword': '12345678Xx',  # Replace with desired password
    'objectClass': ['top', 'person', 'organizationalPerson', 'user'],
}

# Add new user
con.add(new_user_dn, attributes=new_user_attributes)

# Check result
if con.result['result'] == 0:
    print(f"User '{new_user_dn}' successfully added.")
else:
    print(f"Failed to add user '{new_user_dn}'. Error: {con.result['message']}")


