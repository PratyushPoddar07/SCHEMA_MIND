import asyncio
import json
import sys
import os
from unittest.mock import MagicMock, AsyncMock

# Add backend to path
backend_path = os.path.join(os.getcwd(), "backend")
sys.path.append(backend_path)

# Set environment variables BEFORE importing app components
os.environ["DATABASE_URL"] = "sqlite:///test.db"
os.environ["ANTHROPIC_API_KEY"] = "mock_key"
os.environ["SECRET_KEY"] = "mock_secret"

from app.services.ai_service import ai_service
from app.services.query_service import QueryExecutor
from app.schemas.schemas import QueryStatus, SQLGenerationResponse, DataInsight

async def test_full_database_control():
    print("=== Testing Full Database Control (Infrastructure Only) ===")
    
    # Use the local SQLite database for testing
    db_path = os.path.join(os.getcwd(), "backend", "test_data_infra.db")
    connection_string = f"sqlite:///{db_path}"
    executor = QueryExecutor(connection_string)
    
    # Mock AI Service methods
    ai_service.generate_sql = AsyncMock()
    ai_service.generate_insights = AsyncMock()
    
    # 1. Test DDL: Create Table
    print("\n1. Testing DDL Infrastructure: 'Create a table user_tasks'")
    ai_service.generate_sql.return_value = SQLGenerationResponse(
        sql="CREATE TABLE user_tasks (id INTEGER PRIMARY KEY, title TEXT, status TEXT)",
        explanation="Creating a table for tasks",
        confidence=1.0,
        tables_used=["user_tasks"],
        complexity_score=1
    )
    
    sql_result = await ai_service.generate_sql("Create tasks table", {})
    print(f"Mocked SQL: {sql_result.sql}")
    
    exec_result = await executor.execute_query(sql_result.sql, read_only=False)
    print(f"Execution Status: {exec_result['status']}")
    print(f"Execution Results: {exec_result['results']}")
    
    # 2. Test DML: Insert Data
    print("\n2. Testing DML Infrastructure: 'Add a task'")
    ai_service.generate_sql.return_value = SQLGenerationResponse(
        sql="INSERT INTO user_tasks (title, status) VALUES ('Finish AI project', 'pending')",
        explanation="Inserting a task",
        confidence=1.0,
        tables_used=["user_tasks"],
        complexity_score=1
    )
    
    sql_result = await ai_service.generate_sql("Add task", {})
    print(f"Mocked SQL: {sql_result.sql}")
    
    exec_result = await executor.execute_query(sql_result.sql, read_only=False)
    print(f"Execution Status: {exec_result['status']}")
    print(f"Execution Results: {exec_result['results']}")
    
    # 3. Test Select & Interpretation
    print("\n3. Testing SELECT & Insights Infrastructure")
    ai_service.generate_sql.return_value = SQLGenerationResponse(
        sql="SELECT * FROM user_tasks",
        explanation="Selecting all tasks",
        confidence=1.0,
        tables_used=["user_tasks"],
        complexity_score=1
    )
    
    ai_service.generate_insights.return_value = [
        DataInsight(
            type="summary",
            title="Task Summary",
            description="You have one pending task: 'Finish AI project'.",
            confidence=1.0
        )
    ]
    
    sql_result = await ai_service.generate_sql("Get tasks", {})
    exec_result = await executor.execute_query(sql_result.sql, read_only=False)
    print(f"Execution Status: {exec_result['status']}")
    
    if exec_result["status"] == QueryStatus.SUCCESS:
        insights = await ai_service.generate_insights(exec_result["results"], "What tasks do I have?")
        print("\nMocked Plain Language Explanation (Insights):")
        for i in insights:
            print(f"- [{i.type}] {i.title}: {i.description}")

if __name__ == "__main__":
    db_path = os.path.join(os.getcwd(), "backend", "test_data_infra.db")
    if os.path.exists(db_path):
        os.remove(db_path)
    asyncio.run(test_full_database_control())
