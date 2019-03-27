import base64

username='admin@userdb.com'
password='admin'

auth_header = 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')
print(auth_header)
