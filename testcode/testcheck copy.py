from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, SUBTREE

server_address = "ldaps://10.1.55.210:636"
domain = "test"
loginun = "Administrator"
loginpw = "12345678Xx"
base_dn = "guest1"


# Define server connection details
server = Server('ldaps://10.1.55.210:636', use_ssl=True, get_info=ALL)  # Replace with your Active Directory server IP or hostname

# Establish connection
conn = Connection(server, user='test\\Administrator', password='12345678Xx', auto_bind=True)

base_dn = f"OU={base_dn},OU=Guest,DC=test,DC=local"

conn.search(
            search_base=base_dn,
            search_filter="(objectClass=person)",  # Filter for user objects
            search_scope=SUBTREE,
            attributes=["cn"],  # Retrieve only the common name attribute
        )

user_names = [entry.cn.value for entry in conn.entries]

conn.unbind()

print(user_names)