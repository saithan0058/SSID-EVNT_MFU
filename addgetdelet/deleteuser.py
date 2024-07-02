from flask import Flask, jsonify, request
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
base_dn = 'OU=guest1,OU=Guest,DC=test,DC=local'
server_address = "ldaps://10.1.55.210:636"
domain = "test"
loginun = "Administrator"
def delete_all_users():
    try:
        # Connect to LDAP server
        server = Server(server_address, connect_timeout=5, use_ssl=True, get_info=ALL)
        conn = Connection(server, user=f"{domain}\\{loginun}", password=loginpw, authentication=NTLM, auto_bind=True)
        
        # Search for all users
        conn.search(
            search_base=base_dn,
            search_filter='(objectClass=person)',  # Filter for user objects
            search_scope=SUBTREE,
            attributes=[]  # Retrieve all attributes
        )
        
        # Delete each user found
        for entry in conn.entries:
            conn.delete(entry.entry_dn)
        
        # Unbind the connection
        conn.unbind()
        
        return jsonify({'message': 'All users deleted successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
