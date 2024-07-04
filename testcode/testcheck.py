from ldap3 import Server, Connection, ALL, SUBTREE,NTLM

server_address = "ldaps://10.1.55.210:636"
domain = "test"
loginun = "Administrator"
loginpw = "12345678Xx"

# LDAP server details
base_dn = 'OU=guest1,OU=Guest,DC=test,DC=local'  # Adjust for your nested OU
user_dn = 'cn=admin,dc=test,dc=local'  # Adjust according to your setup
password = 'your_password'  # Adjust according to your setup

# Connect to the server
server = Server(server_address, connect_timeout=5, use_ssl=True, get_info=ALL)
conn = Connection(server, user=f"{domain}\\{loginun}", password=loginpw, authentication=NTLM, auto_bind=True)

# Search for all users in the specified nested OU and retrieve their common names (cn)
conn.search(
    search_base=base_dn,
    search_filter='(objectClass=person)',  # Filter for user objects
    search_scope=SUBTREE,
    attributes=['cn']  # Retrieve only the common name attribute
)

# Print the names of users in a numbered list format
for i, entry in enumerate(conn.entries, start=1):
    print(f"{i}. {entry.cn.value}")

# Unbind the connection
conn.unbind()