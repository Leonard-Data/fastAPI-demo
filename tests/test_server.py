import requests

response = requests.get("http://127.0.0.1:8000/items/89")
print(response.json())