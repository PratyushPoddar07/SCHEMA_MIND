from sqlalchemy import create_engine, text
from typing import List, Dict, Any, Optional
import time
import json
from app.core.config import settings
from app.schemas.schemas import QueryStatus
import asyncio
from concurrent.futures import ThreadPoolExecutor


class QueryExecutor:
    """Execute SQL queries safely with timeout and validation"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.is_mongodb = connection_string.startswith(("mongodb://", "mongodb+srv://"))
        
        if self.is_mongodb:
            from pymongo import MongoClient
            from urllib.parse import urlparse
            self.mongo_client = MongoClient(
                connection_string, 
                serverSelectionTimeoutMS=settings.QUERY_TIMEOUT_SECONDS * 1000
            )
            # Correctly handle database name from path
            self.mongo_db_name = settings.MONGODB_URL.split('/')[-1].split('?')[0] if '?' in settings.MONGODB_URL else settings.MONGODB_URL.split('/')[-1]
            if not self.mongo_db_name or self.mongo_db_name == "atlas-sql-6989f8b63bb4d1f488aac3ca":
                # Fallback or correction for Atlas SQL specific weirdness in parsing
                parsed = urlparse(connection_string)
                self.mongo_db_name = parsed.path.lstrip('/') or "sample_mflix"
            
            self.mongo_db = self.mongo_client.get_database(self.mongo_db_name)
            self.is_atlas_sql = ".a.query.mongodb.net" in connection_string
            self.engine = None
        else:
            self.engine = create_engine(
                connection_string,
                pool_pre_ping=True,
                connect_args={"connect_timeout": settings.QUERY_TIMEOUT_SECONDS}
            )
        self.executor = ThreadPoolExecutor(max_workers=5)
    
    async def execute_query(
        self,
        sql: str,
        max_rows: int = 1000
    ) -> Dict[str, Any]:
        """Execute SQL query and return results"""
        
        start_time = time.time()
        
        try:
            if self.is_mongodb:
                # For MongoDB, we support the 'SELECT 1' test and JSON aggregation pipelines
                sql_stripped = sql.strip()
                if sql_stripped.upper() == "SELECT 1":
                    return {
                        "status": QueryStatus.SUCCESS,
                        "results": [{"1": 1}],
                        "execution_time_ms": int((time.time() - start_time) * 1000),
                        "result_count": 1
                    }
                
                # If it's Atlas SQL, we might want to allow direct SQL via their SQL interface
                # However, pymongo itself doesn't speak SQL. 
                # If the user provides SQL for an Atlas SQL connection, 
                # we should explain that this tool currently uses the Aggregation Pipeline
                # OR if we want to support Atlas SQL specifically, we'd need the Atlas SQL driver.
                
                # For now, let's make it smarter: if it looks like SQL (starts with SELECT) 
                # but it's a MongoDB connection, we fail gracefully with a hint.
                if sql_stripped.upper().startswith("SELECT"):
                    if not self.is_atlas_sql:
                        return {
                            "status": QueryStatus.ERROR,
                            "error": "SQL queries are not supported on standard MongoDB. Please use JSON Aggregation Pipeline format.",
                            "results": [],
                            "execution_time_ms": 0
                        }
                    # If it IS atlas sql, we still need to handle it. 
                    # Many users use the MongoDB SQL Translator or Atlas SQL Interface.
                    # Since we are using pymongo, we MUST use pipelines.
                    # AI service should have been instructed to return pipelines for MongoDB.
                
                try:
                    # Try to parse as JSON pipeline
                    pipeline = json.loads(sql_stripped)
                    if not isinstance(pipeline, list):
                        raise ValueError("MongoDB pipeline must be a JSON array")
                    
                    # We need the collection name. If not provided, we try to infer from AI metadata OR use the first collection
                    # For now, let's assume the first stage might indicate the collection or we take it from a wrapper
                    # BETTER: Since AIService returns tables_used, but we only get 'sql' string here,
                    # we'll assume the 'sql' might be wrapped as {"collection": "...", "pipeline": [...]}
                    
                    data = json.loads(sql_stripped)
                    if isinstance(data, dict) and "collection" in data and "pipeline" in data:
                        coll_name = data["collection"]
                        actual_pipeline = data["pipeline"]
                    else:
                        # Fallback: AI generated just the array, we need to find which collection.
                        # As a temporary heuristic, we'll return an error asking for collection if not found.
                        return {
                            "status": QueryStatus.ERROR,
                            "error": "MongoDB query format mismatch. Expected JSON with 'collection' and 'pipeline'.",
                            "results": [],
                            "execution_time_ms": 0
                        }

                    results = list(self.mongo_db[coll_name].aggregate(actual_pipeline))
                    # Serialize ObjectIds
                    for doc in results:
                        if "_id" in doc:
                            doc["_id"] = str(doc["_id"])
                    
                    return {
                        "status": QueryStatus.SUCCESS,
                        "results": results,
                        "execution_time_ms": int((time.time() - start_time) * 1000),
                        "result_count": len(results)
                    }
                except Exception as mongo_err:
                    return {
                        "status": QueryStatus.ERROR,
                        "error": f"MongoDB Aggregation Error: {str(mongo_err)}",
                        "results": [],
                        "execution_time_ms": 0
                    }

            # Validate query
            if not self._is_safe_query(sql):
                return {
                    "status": QueryStatus.ERROR,
                    "error": "Unsafe query detected. Only SELECT statements are allowed.",
                    "results": [],
                    "execution_time_ms": 0
                }
            
            # Execute in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                self.executor,
                self._execute_sync,
                sql,
                max_rows
            )
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return {
                "status": QueryStatus.SUCCESS,
                "results": results,
                "execution_time_ms": execution_time,
                "result_count": len(results)
            }
            
        except Exception as e:
            execution_time = int((time.time() - start_time) * 1000)
            return {
                "status": QueryStatus.ERROR,
                "error": str(e),
                "results": [],
                "execution_time_ms": execution_time,
                "result_count": 0
            }
    
    def _execute_sync(self, sql: str, max_rows: int) -> List[Dict[str, Any]]:
        """Synchronous query execution"""
        if self.is_mongodb:
            return [] # Should be handled in execute_query
            
        with self.engine.connect() as conn:
            result = conn.execute(text(sql))
            
            # Fetch results
            rows = []
            for i, row in enumerate(result):
                if i >= max_rows:
                    break
                rows.append(dict(row._mapping))
            
            return rows
    
    def _is_safe_query(self, sql: str) -> bool:
        """Validate that query is safe (read-only)"""
        sql_upper = sql.upper().strip()
        
        # Forbidden keywords
        forbidden = [
            "INSERT", "UPDATE", "DELETE", "DROP", "CREATE",
            "ALTER", "TRUNCATE", "GRANT", "REVOKE", "EXEC"
        ]
        
        # Check if query starts with SELECT or WITH (for CTEs)
        if not (sql_upper.startswith("SELECT") or sql_upper.startswith("WITH")):
            return False
        
        # Check for forbidden keywords
        for keyword in forbidden:
            if keyword in sql_upper:
                return False
        
        return True
    
    async def test_connection(self) -> bool:
        """Test database connection. Raises exception if failed."""
        if self.is_mongodb:
            self.mongo_client.admin.command('ping')
            return True
        
        with self.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    
    def close(self):
        """Close database connection"""
        if self.is_mongodb:
            self.mongo_client.close()
        elif self.engine:
            self.engine.dispose()


class QueryValidator:
    """Validate and sanitize SQL queries"""
    
    @staticmethod
    def validate_complexity(sql: str) -> Dict[str, Any]:
        """Analyze query complexity"""
        sql_upper = sql.upper()
        
        complexity_score = 0
        issues = []
        
        # Count JOINs
        join_count = sql_upper.count("JOIN")
        complexity_score += join_count * 2
        
        # Count subqueries
        subquery_count = sql_upper.count("SELECT") - 1
        complexity_score += subquery_count * 3
        
        # Check for complex operations
        if "GROUP BY" in sql_upper:
            complexity_score += 1
        if "HAVING" in sql_upper:
            complexity_score += 1
        if "UNION" in sql_upper:
            complexity_score += 2
        if "DISTINCT" in sql_upper:
            complexity_score += 1
        
        # Check complexity threshold
        if complexity_score > settings.MAX_QUERY_COMPLEXITY:
            issues.append(f"Query complexity ({complexity_score}) exceeds maximum ({settings.MAX_QUERY_COMPLEXITY})")
        
        # Check for missing LIMIT
        if "LIMIT" not in sql_upper and "TOP" not in sql_upper:
            issues.append("Consider adding LIMIT clause to prevent large result sets")
        
        return {
            "complexity_score": complexity_score,
            "is_valid": len(issues) == 0 or complexity_score <= settings.MAX_QUERY_COMPLEXITY,
            "issues": issues,
            "suggestions": QueryValidator._get_optimization_suggestions(sql)
        }
    
    @staticmethod
    def _get_optimization_suggestions(sql: str) -> List[str]:
        """Get optimization suggestions for query"""
        suggestions = []
        sql_upper = sql.upper()
        
        if "SELECT *" in sql_upper:
            suggestions.append("Specify exact columns instead of SELECT * for better performance")
        
        if sql_upper.count("JOIN") > 3:
            suggestions.append("Multiple JOINs detected - ensure proper indexes exist")
        
        if "OR" in sql_upper:
            suggestions.append("OR conditions may prevent index usage - consider using UNION instead")
        
        if "LIKE '%'" in sql_upper:
            suggestions.append("Leading wildcards in LIKE prevent index usage")
        
        return suggestions
    
    @staticmethod
    def add_safety_limits(sql: str, max_rows: int = 1000) -> str:
        """Add safety limits to query"""
        sql_upper = sql.upper()
        
        if "LIMIT" not in sql_upper and "TOP" not in sql_upper:
            sql = sql.rstrip(";")
            sql += f" LIMIT {max_rows}"
        
        return sql
