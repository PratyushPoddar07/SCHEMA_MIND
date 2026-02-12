from pymongo import MongoClient
import sys

def diagnose():
    # Constructing the URI with provided credentials
    uri = "mongodb://PratyushPoddar:PratyushPoddar@atlas-sql-6989f8b63bb4d1f488aac3ca-am4zg5.a.query.mongodb.net/?ssl=true&authSource=admin&appName=atlas-sql-6989f8b63bb4d1f488aac3ca"
    
    print(f"Diagnosing URI (obfuscated): mongodb://PratyushPoddar:***@...")
    try:
        # Standard client
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        
        print("Checking ping on cluster...")
        try:
            client.admin.command('ping')
            print("✅ Global ping success")
        except Exception as e:
            print(f"❌ Global ping failed: {e}")

        print("Listing databases...")
        try:
            dbs = client.list_database_names()
            print(f"✅ Databases: {dbs}")
            
            for db_name in dbs:
                if db_name in ['admin', 'local', 'config']: continue
                print(f"Checking collections in {db_name}...")
                db = client.get_database(db_name)
                colls = db.list_collection_names()
                print(f"✅ Collections in {db_name}: {colls}")
        except Exception as e:
            print(f"❌ database/collection listing failed: {e}")
            
    except Exception as e:
        print(f"❌ CRITICAL Error: {str(e)}")

if __name__ == "__main__":
    diagnose()
