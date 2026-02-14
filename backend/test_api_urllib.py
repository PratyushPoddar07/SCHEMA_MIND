import urllib.request
import json

url = "http://localhost:8000/api/v1/databases"
data = {
    "name": "test_script_db",
    "db_type": "postgresql",
    "connection_string": "postgresql://postgres:7815052095@localhost:5433/postgres"
}
headers = {'Content-Type': 'application/json'}

print(f"Testing POST to {url} with data: {data}")

req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        print(f"Status: {response.getcode()}")
        print("Response:", response.read().decode())
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code}")
    print("Error Body:", e.read().decode())
except Exception as e:
    print(f"Error: {e}")
