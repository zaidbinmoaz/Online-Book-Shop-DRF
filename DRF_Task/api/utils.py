import requests

def get_data():
    url = 'http://127.0.0.1:8000/EpicBooks/'
    response = requests.get(url)
    data = response.json()
    return data