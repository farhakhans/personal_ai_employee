import requests
r = requests.get('http://localhost:5000')
print('Status', r.status_code)
text = r.text
print('Email or Username present?', 'Email or Username' in text)
print('Demo credentials present?', 'Demo Credentials' in text)
print('payload username snippet present?', 'username' in text and 'email' in text)
# print sample lines containing keyword
for line in text.splitlines():
    if 'Email or Username' in line or 'payload' in line or 'Demo Credentials' in line:
        print('>>', line)
