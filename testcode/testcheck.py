from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, SUBTREE

server_address = "ldaps://10.1.55.210:636"
domain = "test"
loginun = "Administrator"
loginpw = "12345678Xx"
base_dn = f"dc={domain},dc=local"
guest_dn = f"ou=Guest,{base_dn}"

# Define server connection details
server = Server('ldaps://10.1.55.210:636', use_ssl=True, get_info=ALL)  # Replace with your Active Directory server IP or hostname

# Establish connection
conn = Connection(server, user='test\\Administrator', password='12345678Xx', auto_bind=True)

# ฟังก์ชันสำหรับดึงรายชื่อ OU ทั้งหมดใน OU=Guest
def get_ous_in_guest():
    conn.search(guest_dn, '(objectClass=organizationalUnit)', attributes=['ou'])
    return [entry.entry_dn for entry in conn.entries]

# ฟังก์ชันสำหรับตรวจสอบว่า OU มีผู้ใช้หรือไม่
def has_users(ou_dn):
    conn.search(ou_dn, '(objectClass=person)', search_scope=SUBTREE)
    return len(conn.entries) > 0

# ดึงรายชื่อ OU ทั้งหมดใน OU=Guest
ous_in_guest = get_ous_in_guest()

# ตรวจสอบ OU ใน OU=Guest ที่ไม่มีผู้ใช้
ous_without_users = [ou.split(",")[0].split("=")[1] for ou in ous_in_guest if not has_users(ou)]

# แสดงผลลัพธ์
print("OUs in Guest without users:")
for ou in ous_without_users:
    print(ou)

# ปิดการเชื่อมต่อ
conn.unbind()