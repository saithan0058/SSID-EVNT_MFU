from ldap3 import Server, Connection, ALL, MODIFY_REPLACE

# Define server connection details
server = Server('ldaps://10.1.55.210:636', use_ssl=True, get_info=ALL)  # Replace with your Active Directory server IP or hostname

# Establish connection
con = Connection(server, user='test\\Administrator', password='12345678Xx', auto_bind=True)

# Define user DN and attribute change
user_dn = 'CN=james,OU=Guest,DC=test,DC=local'
changes = {
    'userAccountControl': [(MODIFY_REPLACE, [66048])]  # 66048 is the value for normal user without password change at next logon
}

try:
    # Modify user attributes
    con.modify(user_dn, changes)

    # Check result
    if con.result['result'] == 0:
        print(f"Successfully removed 'User must change password at next logon' for '{user_dn}'.")
    else:
        print(f"Failed to modify '{user_dn}'. Error: {con.result['message']}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Always unbind the connection
    con.unbind()
