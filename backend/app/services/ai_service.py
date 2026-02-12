from anthropic import Anthropic
from typing import Dict, Any, List, Optional
import json
from app.core.config import settings
from app.schemas.schemas import SQLGenerationResponse, DataInsight
import re


class AIService:
    """AI service for natural language processing and SQL generation"""
    
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = "claude-sonnet-4-20250514"
    
    async def generate_sql(
        self,
        natural_language: str,
        schema_info: Dict[str, Any],
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> SQLGenerationResponse:
        """Generate SQL or MongoDB query from natural language query"""
        
        db_type = schema_info.get("database_type", "postgresql").lower()
        is_mongodb = db_type == "mongodb"
        
        # Build context from schema
        schema_context = self._build_schema_context(schema_info)
        
        # Build conversation context
        conversation_context = ""
        if conversation_history:
            conversation_context = "\n\nPrevious conversation:\n"
            for msg in conversation_history[-5:]:  # Last 5 messages
                conversation_context += f"{msg['role']}: {msg['content']}\n"
        
        if is_mongodb:
            query_type = "MongoDB Aggregation Pipeline (JSON)"
            syntax_rules = """
1. Use MongoDB aggregation pipeline syntax as a JSON array
2. Use $match, $group, $project, $lookup, $sort, $limit, etc.
3. IMPORTANT: For MongoDB, the "sql" field must be a JSON object containing:
   {"collection": "target_collection_name", "pipeline": [...]}
4. Optimize for performance
"""
        else:
            query_type = "precise SQL query"
            syntax_rules = """
1. Use proper SQL syntax for the database type
2. Include appropriate WHERE clauses, JOINs, and aggregations
3. Optimize for performance
4. Return ONLY valid SQL
"""

        prompt = f"""You are an expert database query generator. Convert the natural language question into a {query_type}.

Database Type: {db_type}
Database Schema:
{schema_context}
{conversation_context}

User Question: {natural_language}

Rules:
{syntax_rules}
5. Return ONLY valid response, no explanations in the query itself

Respond in JSON format:
{{
    "sql": "Actual query string or JSON array string",
    "explanation": "Step-by-step explanation of the query logic",
    "confidence": 0.95,
    "tables_used": ["collection_name_or_table"],
    "complexity_score": 5
}}
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse response
        content = response.content[0].text
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            # Fallback parsing
            result = {
                "sql": content.strip(),
                "explanation": "Query generated",
                "confidence": 0.8,
                "tables_used": [],
                "complexity_score": 5
            }
        
        return SQLGenerationResponse(**result)
    
    async def generate_insights(
        self,
        query_results: List[Dict[str, Any]],
        original_question: str
    ) -> List[DataInsight]:
        """Generate AI-powered insights from query results"""
        
        if not query_results:
            return []
        
        # Prepare data summary
        data_summary = {
            "row_count": len(query_results),
            "columns": list(query_results[0].keys()) if query_results else [],
            "sample_data": query_results[:5]
        }
        
        prompt = f"""Analyze the following data and provide intelligent insights.

Original Question: {original_question}

Data Summary:
{json.dumps(data_summary, indent=2, default=str)}

Provide insights in JSON format as an array:
[
    {{
        "type": "trend|anomaly|pattern|summary",
        "title": "Brief title",
        "description": "Detailed insight",
        "confidence": 0.0-1.0
    }}
]

Focus on:
- Notable trends or patterns
- Anomalies or outliers
- Key statistics
- Actionable recommendations
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        
        # Extract JSON array
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        if json_match:
            insights_data = json.loads(json_match.group())
            return [DataInsight(**insight) for insight in insights_data]
        
        return []
    
    async def explain_sql(self, sql: str, schema_info: Dict[str, Any]) -> str:
        """Explain SQL query in plain language"""
        
        prompt = f"""Explain this SQL query in simple, non-technical language:

SQL Query:
{sql}

Database Schema:
{self._build_schema_context(schema_info)}

Provide a clear explanation that a non-technical person can understand.
Focus on:
1. What data is being retrieved
2. Which tables are involved
3. Any filtering or grouping logic
4. The purpose of the query
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    async def suggest_visualizations(
        self,
        query_results: List[Dict[str, Any]],
        original_question: str
    ) -> List[str]:
        """Suggest appropriate visualization types for the data"""
        
        if not query_results:
            return []
        
        columns = list(query_results[0].keys()) if query_results else []
        
        prompt = f"""Based on the following data, suggest appropriate visualization types:

Original Question: {original_question}
Columns: {', '.join(columns)}
Row Count: {len(query_results)}

Suggest 2-3 visualization types from:
- bar_chart
- line_chart
- pie_chart
- scatter_plot
- 3d_scatter
- heatmap
- table
- area_chart

Return as JSON array: ["type1", "type2", "type3"]
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        
        return ["table"]
    
    def _build_schema_context(self, schema_info: Dict[str, Any]) -> str:
        """Build a readable schema context for the AI"""
        context = []
        
        tables = schema_info.get("tables", {})
        for table_name, table_data in tables.items():
            columns_str = ", ".join([
                f"{col['name']} ({col['type']})"
                for col in table_data.get("columns", [])
            ])
            context.append(f"Table: {table_name}\nColumns: {columns_str}\n")
        
        return "\n".join(context)
    
    async def optimize_query(self, sql: str, schema_info: Dict[str, Any]) -> str:
        """Suggest query optimizations"""
        
        prompt = f"""Analyze this SQL query and suggest optimizations:

{sql}

Schema:
{self._build_schema_context(schema_info)}

Provide optimization suggestions for:
- Index usage
- JOIN optimization
- Query structure
- Performance improvements
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text


# Singleton instance
ai_service = AIService()
