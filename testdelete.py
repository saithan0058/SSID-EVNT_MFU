from ldap3 import Server, Connection, ALL, SUBTREE

# Define server connection details
server = Server(
    "ldaps://10.1.55.210:636"
)  # Replace with your Active Directory server IP or hostname

# Establish connection
con = Connection(
    server, user="test\\Administrator", password="12345678Xx", auto_bind=True
)
UOunder = "guest1"
# Define the base DN for the search
base_dn = f"OU={UOunder},OU=Guest,DC=test,DC=local"  # Replace with your target OU

# Search for all users in the specified OU
con.search(
    search_base=base_dn,
    search_filter="(objectClass=user)",
    search_scope=SUBTREE,
    attributes=["distinguishedName"],
)

# Iterate through the search results and delete each user
for entry in con.entries:
    user_dn = entry.distinguishedName.value
    con.delete(user_dn)
    if con.result["result"] == 0:
        print(f"User '{user_dn}' successfully deleted.")
    else:
        print(f"Failed to delete user '{user_dn}'. Error: {con.result['message']}")

# Unbind the connection
con.unbind()
