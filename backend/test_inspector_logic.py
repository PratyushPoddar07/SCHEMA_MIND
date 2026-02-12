from pymongo import MongoClient
from urllib.parse import urlparse
import sys

def test_inspector_logic_fixed():
    uri = "mongodb://PratyushPoddar:PratyushPoddar@atlas-sql-6989f8b63bb4d1f488aac3ca-am4zg5.a.query.mongodb.net/?ssl=true&authSource=admin&appName=atlas-sql-6989f8b63bb4d1f488aac3ca"
    print(f"Testing FIXED Inspector logic for: {uri}")
    
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        parsed = urlparse(uri)
        # THE FIX: use 'or' instead of 'if/else' check on path
        db_name = parsed.path.lstrip('/') or "test"
        print(f"Targeting database: {db_name}")
        
        db = client.get_database(db_name)
        
        print("Listing collections...")
        # Note: If targeting 'test' and it doesn't exist, this might still return empty or fail depending on Atlas permissions
        # But it should NOT crash with InvalidName anymore.
        colls = db.list_collection_names()
        print(f"✅ Collections found: {colls}")
        
        print("🎉 Logic verified")
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_inspector_logic_fixed()
