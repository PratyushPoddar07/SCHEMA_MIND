import urllib.request
import json

url = "http://localhost:8000/api/v1/query"
data = {
    "natural_language_query": "List all tables",
    "database_id": 7,
    "include_insights": False,
    "explain_sql": False
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
