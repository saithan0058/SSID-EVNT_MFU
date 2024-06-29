from ldap3 import Server, Connection, ALL, MODIFY_REPLACE, NTLM

domain = 'test'
loginun = 'Administrator'
loginpw = '12345678Xx'

username = 'john.smith'
useremail = 'john@smith.com'
userpswd = '12345678Xx'
userdn = 'CN=john,OU=Guest,DC=test,DC=local'

# connect - specifying port 636 is only for reference as it's inferred
s = Server('ldaps://10.1.55.210:636', connect_timeout=5, use_ssl=True, get_info=ALL)
c = Connection(s, user='test\\Administrator', password=loginpw, authentication=NTLM)

if not c.bind():
    exit(c.result)

# create user
c.add(userdn, attributes={
    'cn': 'john',
    'givenName': 'john',
    'sn': 'User',
    'displayName': username,
    'userPrincipalName': 'john@test.local',
    'sAMAccountName': 'john',
    'userPassword': userpswd,  # Replace with desired password
    'objectClass': ['top', 'person', 'organizationalPerson', 'user'],
})

# set password - must be done before enabling user
# you must connect with SSL to set the password 
c.extend.microsoft.modify_password(userdn, userpswd)

# enable user (after password set)
c.modify(userdn, {'userAccountControl': [('MODIFY_REPLACE', 512)]})

# ena user
c.modify(userdn, {'userAccountControl': [('MODIFY_REPLACE', 64)]})

# Check result
if c.result['result'] == 0:
    print(f"User '{userdn}' successfully added.")
else:
    print(f"Failed to add user '{userdn}'. Error: {c.result['message']}")