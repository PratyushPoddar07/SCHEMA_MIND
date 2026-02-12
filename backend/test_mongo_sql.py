import os
import sys
from sqlalchemy import create_engine
from dotenv import load_dotenv

def test():
    url = "mongodb://atlas-sql-6989f8b63bb4d1f488aac3ca-am4zg5.a.query.mongodb.net/myVirtualDatabase?ssl=true&authSource=admin"
    print(f"Testing URL: {url}")
    try:
        engine = create_engine(url)
        conn = engine.connect()
        print("✅ Success: Connected to MongoDB Atlas SQL")
        conn.close()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(f"Error Type: {type(e).__name__}")

if __name__ == "__main__":
    test()
