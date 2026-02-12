import requests
import json

print("=" * 60)
print("FULL END-TO-END VERIFICATION")
print("=" * 60)

# Test 1: Backend health via direct call
print("\n1. Backend Health (direct)...")
try:
    r = requests.get("http://localhost:8000/health", timeout=5)
    print(f"   ✅ Status: {r.status_code} -> {r.json()}")
except Exception as e:
    print(f"   ❌ {e}")

# Test 2: Backend health via Vite proxy (same as frontend)
print("\n2. Backend Health (via Vite proxy localhost:5173)...")
try:
    r = requests.get("http://localhost:5173/api/v1/databases", timeout=5)
    print(f"   ✅ Status: {r.status_code}")
    print(f"   Response: {r.text[:200]}")
except Exception as e:
    print(f"   ❌ {e}")

# Test 3: Create MongoDB database via Vite proxy
print("\n3. Creating MongoDB database (via Vite proxy)...")
payload = {
    "name": "Atlas Movies",
    "db_type": "mongodb",
    "connection_string": "mongodb://PratyushPoddar:PratyushPoddar@atlas-sql-6989f8b63bb4d1f488aac3ca-am4zg5.a.query.mongodb.net/sample_mflix?ssl=true&authSource=admin"
}
try:
    r = requests.post("http://localhost:5173/api/v1/databases", json=payload, timeout=30)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.text[:500]}")
    if r.status_code == 200:
        print("   ✅ DATABASE CREATED SUCCESSFULLY!")
    else:
        print(f"   ❌ FAILED: {r.status_code}")
except Exception as e:
    print(f"   ❌ {e}")

# Test 4: List all databases
print("\n4. Listing all databases...")
try:
    r = requests.get("http://localhost:8000/api/v1/databases", timeout=5)
    print(f"   Status: {r.status_code}")
    dbs = r.json()
    for db in dbs:
        print(f"   📂 [{db['id']}] {db['name']} ({db['db_type']}) - Active: {db['is_active']}")
    print(f"   ✅ Total databases: {len(dbs)}")
except Exception as e:
    print(f"   ❌ {e}")

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
