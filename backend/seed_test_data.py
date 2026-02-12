import os
import sys
from sqlalchemy import create_engine, text
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")
MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_URL = os.getenv("DATABASE_URL")

# Sample Data
PRODUCTS = [
    ("Quantum Laptop", "Electronics", 1299.99, 45),
    ("Nebula Phone", "Electronics", 799.50, 120),
    ("Z-Gear Smartwatch", "Electronics", 199.00, 250),
    ("Eco-Friendly Bottle", "Lifestyle", 25.00, 500),
    ("Ergonomic Chair", "Furniture", 350.00, 15),
    ("Mechanical Keyboard", "Electronics", 120.00, 80),
    ("Wireless Mouse", "Electronics", 45.00, 200),
    ("Gaming Headset", "Electronics", 85.00, 60),
    ("Desk Lamp", "Furniture", 35.00, 150),
    ("Canvas Backpack", "Lifestyle", 55.00, 300)
]

def seed_sql(db_url, name="SQL"):
    print(f"--- Seeding {name} ---")
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS sample_products (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    category VARCHAR(100),
                    price DECIMAL(10, 2),
                    stock_quantity INTEGER
                );
            """))
            conn.execute(text("TRUNCATE TABLE sample_products RESTART IDENTITY CASCADE;"))
            for p in PRODUCTS:
                conn.execute(text("INSERT INTO sample_products (name, category, price, stock_quantity) VALUES (:n, :c, :p, :s)"),
                           {"n": p[0], "c": p[1], "p": p[2], "s": p[3]})
            conn.commit()
            print(f"✅ Success: Sample data seeded into {name}")
    except Exception as e:
        print(f"❌ Error seeding {name}: {str(e)}")

def seed_mongodb():
    print("--- Seeding MongoDB Atlas ---")
    if not MONGODB_URL or "<username>" in MONGODB_URL:
        print("❌ Skip: MONGODB_URL not configured correctly.")
        return
    
    try:
        client = MongoClient(MONGODB_URL)
        db = client.get_database("test_analytics")
        collection = db.get_collection("products")
        
        # Clear existing
        collection.delete_many({})
        
        # Insert
        docs = [{"name": p[0], "category": p[1], "price": p[2], "stock_quantity": p[3]} for p in PRODUCTS]
        collection.insert_many(docs)
        print("✅ Success: Sample data seeded into MongoDB Atlas (database: test_analytics, collection: products)")
    except Exception as e:
        print(f"❌ Error seeding MongoDB: {str(e)}")

if __name__ == "__main__":
    # 1. Try PostgreSQL (Local)
    if DATABASE_URL:
        seed_sql(DATABASE_URL, "PostgreSQL")
    
    # 2. Seed SQLite (Always Works)
    sqlite_url = "sqlite:///test_data.db"
    seed_sql(sqlite_url, "SQLite")
    
    # 3. Seed MongoDB Atlas
    seed_mongodb()
    
    print("\n--- SEEDING COMPLETE ---")
    print("You can now test the app with the database connections!")
