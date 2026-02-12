from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    queries = relationship("Query", back_populates="user")
    databases = relationship("DatabaseConnection", back_populates="user")


class DatabaseConnection(Base):
    """Database connection model"""
    __tablename__ = "database_connections"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    db_type = Column(String(50), nullable=False)  # postgresql, mysql, mongodb, sqlite
    connection_string = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    schema_cache = Column(JSON, nullable=True)
    last_sync = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="databases")
    queries = relationship("Query", back_populates="database")


class Query(Base):
    """Query history model"""
    __tablename__ = "queries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    database_id = Column(Integer, ForeignKey("database_connections.id"), nullable=False)
    natural_language_query = Column(Text, nullable=False)
    generated_sql = Column(Text, nullable=False)
    execution_time_ms = Column(Integer, nullable=True)
    result_count = Column(Integer, nullable=True)
    status = Column(String(50), default="success")  # success, error, timeout
    error_message = Column(Text, nullable=True)
    insights = Column(JSON, nullable=True)
    context = Column(JSON, nullable=True)  # Conversation context
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="queries")
    database = relationship("DatabaseConnection", back_populates="queries")


class Conversation(Base):
    """Conversation session model"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    database_id = Column(Integer, ForeignKey("database_connections.id"), nullable=False)
    title = Column(String(255), nullable=True)
    context = Column(JSON, nullable=True)  # Stores conversation state
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class QueryTemplate(Base):
    """Saved query templates"""
    __tablename__ = "query_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    natural_language_template = Column(Text, nullable=False)
    sql_template = Column(Text, nullable=False)
    parameters = Column(JSON, nullable=True)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class SchemaEmbedding(Base):
    """Vector embeddings for schema elements"""
    __tablename__ = "schema_embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    database_id = Column(Integer, ForeignKey("database_connections.id"), nullable=False)
    table_name = Column(String(255), nullable=False)
    column_name = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    embedding_id = Column(String(255), nullable=False)  # Reference to vector DB
    created_at = Column(DateTime, default=datetime.utcnow)
