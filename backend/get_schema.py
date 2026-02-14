import urllib.request
import json

url = "http://localhost:8000/api/v1/databases/7/schema"

try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")
