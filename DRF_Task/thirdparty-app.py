import requests

# Replace with your actual API URL and JWT
url = 'http://127.0.0.1:8000/epicbooks/'
token = 'Your_JWT'

headers = {
    'Authorization': f'Bearer {token}',
}

response = requests.get(url, headers=headers)

# Handle the response
if response.status_code == 200:
    data = response.json()
    # Process the data
else:
    print(f'Request failed with status code {response.status_code}')