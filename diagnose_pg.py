import sqlalchemy
from sqlalchemy import create_engine, text
import sys

def test_conn(uri):
    print(f"Testing connection to: {uri}")
    try:
        engine = create_engine(uri, connect_args={"connect_timeout": 5})
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Success!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_conn(sys.argv[1])
    else:
        test_conn("postgresql://postgres:7815052095@localhost:5433/postgres")
