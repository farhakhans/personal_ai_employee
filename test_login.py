import requests
import json

# Test login endpoint
url = 'http://localhost:5000/api/auth/login'
data = {
    'email': 'admin@employee.ai',
    'password': 'Admin@2026!'
}

print('Testing login API...')
print(f'URL: {url}')
print(f'Data: {data}')
print()

try:
    response = requests.post(url, json=data)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {json.dumps(response.json(), indent=2)}')
except Exception as e:
    print(f'Error: {e}')
