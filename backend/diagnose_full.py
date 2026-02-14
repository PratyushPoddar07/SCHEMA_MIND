import sys
import os
import asyncio
import logging

# Configure logging to file
logging.basicConfig(
    filename='diagnosis.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

# Add backend to path
backend_path = os.path.join(os.getcwd(), "backend")
sys.path.append(backend_path)

# Set dummy env for Pydantic
os.environ["DATABASE_URL"] = "sqlite:///test.db"
os.environ["MONGODB_URL"] = "mongodb://localhost:27017"
os.environ["ANTHROPIC_API_KEY"] = "mock"
os.environ["SECRET_KEY"] = "mock"

from app.services.query_service import QueryExecutor
from app.db.database import DatabaseInspector

async def diagnose(uri):
    logging.info(f"--- Diagnosing URI: {uri} ---")
    
    # 1. Test QueryExecutor.test_connection
    logging.info("Step 1: Testing QueryExecutor.test_connection()...")
    try:
        executor = QueryExecutor(uri)
        is_connected = await executor.test_connection()
        logging.info(f"Result: {is_connected}")
        executor.close()
    except Exception as e:
        logging.error(f"FAILED Step 1: {e}", exc_info=True)
        return

    # 2. Test DatabaseInspector
    logging.info("\nStep 2: Testing DatabaseInspector initialization...")
    try:
        inspector = DatabaseInspector(uri)
        logging.info("Success: Inspector initialized")
    except Exception as e:
        logging.error(f"FAILED Step 2: {e}", exc_info=True)
        return

    # 3. Test Schema Sync
    logging.info("\nStep 3: Testing get_schema_info()...")
    try:
        logging.info("Getting table names...")
        table_names = inspector.inspector.get_table_names()
        logging.info(f"Found {len(table_names)} tables: {table_names}")
        
        # Test full schema info
        logging.info("Getting full schema info...")
        schema_info = inspector.get_schema_info()
        logging.info(f"Success: Found {len(schema_info.get('tables', {}))} tables in schema info")
    except Exception as e:
        logging.error(f"FAILED Step 3: {e}", exc_info=True)
        return

    logging.info("\n✅ All backend steps passed for this URI!")

if __name__ == "__main__":
    uri = "postgresql://postgres:7815052095@localhost:5433/postgres"
    if len(sys.argv) > 1:
        uri = sys.argv[1]
    
    asyncio.run(diagnose(uri))
