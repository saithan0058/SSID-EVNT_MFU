from flask import Flask, jsonify
from ldap3 import Server, Connection, ALL, SUBTREE

app = Flask(__name__)

server_address = "ldaps://10.1.55.210:636"
domain = "test"
loginun = "Administrator"
loginpw = "12345678Xx"

@app.route("/get_users/<base_dn>", methods=["GET"])  # get user list เช็ครายชื่อใน ou นั้นๆ
def get_users(base_dn):
    try:
        # Define server connection details
        server = Server(server_address, use_ssl=True, get_info=ALL)

        # Establish connection
        conn = Connection(server, user=f'{domain}\\{loginun}', password=loginpw, auto_bind=True)

        # Define the base DN based on the provided OU name
        search_base_dn = f"OU={base_dn},OU=Guest,DC={domain},DC=local"

        # Search for all users in the specified nested OU and retrieve their common names (cn)
        conn.search(
            search_base=search_base_dn,
            search_filter="(objectClass=person)",  # Filter for user objects
            search_scope=SUBTREE,
            attributes=["cn"],  # Retrieve only the common name attribute
        )

        # Store user names in a list
        user_names = [entry.cn.value for entry in conn.entries]

        # Unbind the connection
        conn.unbind()

        # Return user names as JSON response
        return jsonify({"users": user_names})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
