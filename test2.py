import ldap3

# Set the LDAP server details
ldap_server = 'ldap://192.168.234.129'
ldap_admin_username = 'cn=admin,dc=example,dc=com'
ldap_admin_password = '123'
ldap_base_dn = 'ou=people,dc=example,dc=com'

# Create a connection to the LDAP server and bind as the admin user
server = ldap3.Server(ldap_server)
conn = ldap3.Connection(server, user=ldap_admin_username, password=ldap_admin_password)
conn.bind()

# Perform the search for all entries
conn.search(search_base=ldap_base_dn, search_filter='(objectClass=*)', attributes=['*'])

# Print the search results
for entry in conn.entries:
    print(entry)

# Unbind from the LDAP server
conn.unbind()
