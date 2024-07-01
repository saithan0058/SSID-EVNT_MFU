from ldap3 import Server, Connection, ALL

# Define server connection details
server = Server('ldaps://10.1.55.210:636')  # Replace with your Active Directory server IP or hostname

# Establish connection
con = Connection(server, user='test\\Administrator', password='12345678Xx', auto_bind=True)

# Define user DN to delete
user_dn = 'CN=john,OU=Guest,DC=test,DC=local'  # Replace with the user's DN

# Delete the user
con.delete(user_dn)

# Check result
if con.result['result'] == 0:
    print(f"User '{user_dn}' successfully deleted.")
else:
    print(f"Failed to delete user '{user_dn}'. Error: {con.result['message']}")
