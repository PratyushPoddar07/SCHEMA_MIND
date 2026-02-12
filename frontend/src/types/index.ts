export interface Query {
  id: number;
  natural_language_query: string;
  generated_sql: string;
  execution_time_ms?: number;
  result_count?: number;
  status: 'success' | 'error' | 'timeout' | 'processing';
  results?: any[];
  insights?: QueryInsights;
  sql_explanation?: string;
  visualization_suggestions?: string[];
  created_at: string;
}

export interface QueryInsights {
  insights: DataInsight[];
  count: number;
}

export interface DataInsight {
  type: 'trend' | 'anomaly' | 'pattern' | 'summary';
  title: string;
  description: string;
  confidence: number;
  data_points?: any[];
}

export interface DatabaseConnection {
  id: number;
  name: string;
  db_type: 'postgresql' | 'mysql' | 'mongodb' | 'sqlite';
  is_active: boolean;
  last_sync?: string;
  created_at: string;
}

export interface SchemaInfo {
  tables: Record<string, TableInfo>;
  relationships: Relationship[];
  database_type: string;
  total_tables: number;
}

export interface TableInfo {
  name: string;
  columns: ColumnInfo[];
  foreign_keys: any[];
  indexes: any[];
  sample_data?: any[];
}

export interface ColumnInfo {
  name: string;
  type: string;
  nullable: boolean;
  primary_key: boolean;
  default?: string;
}

export interface Relationship {
  from_table: string;
  from_columns: string[];
  to_table: string;
  to_columns: string[];
}

export interface QueryRequest {
  natural_language_query: string;
  database_id: number;
  conversation_id?: number;
  include_insights?: boolean;
  explain_sql?: boolean;
}

export interface ChartData {
  labels: string[];
  datasets: Dataset[];
}

export interface Dataset {
  label: string;
  data: number[];
  backgroundColor?: string | string[];
  borderColor?: string;
  borderWidth?: number;
}

export interface User {
  id: number;
  email: string;
  username: string;
  is_active: boolean;
  created_at: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}
