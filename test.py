import requests

# test home endpoint
try:
    response = requests.get('http://localhost:5001/')
    print(f"Home endpoint status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")