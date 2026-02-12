# Project Structure

## Complete Directory Tree

```
querymind-ai/
│
├── 📁 backend/                          # FastAPI Backend
│   ├── 📁 app/
│   │   ├── 📁 api/                     # API Endpoints
│   │   │   └── query_routes.py        # Query execution endpoints
│   │   │
│   │   ├── 📁 core/                    # Core Configuration
│   │   │   └── config.py              # Settings & environment variables
│   │   │
│   │   ├── 📁 db/                      # Database Layer
│   │   │   └── database.py            # DB connections & schema inspection
│   │   │
│   │   ├── 📁 models/                  # SQLAlchemy Models
│   │   │   └── models.py              # User, Query, Database models
│   │   │
│   │   ├── 📁 schemas/                 # Pydantic Schemas
│   │   │   └── schemas.py             # Request/response validation
│   │   │
│   │   ├── 📁 services/                # Business Logic
│   │   │   ├── ai_service.py          # AI/Claude integration
│   │   │   └── query_service.py       # SQL execution & validation
│   │   │
│   │   └── 📁 utils/                   # Utilities
│   │
│   ├── main.py                         # FastAPI application entry
│   ├── requirements.txt                # Python dependencies
│   ├── Dockerfile                      # Docker image definition
│   └── .env.example                    # Environment variables template
│
├── 📁 frontend/                         # React Frontend
│   ├── 📁 src/
│   │   ├── 📁 components/              # React Components
│   │   │   ├── Background3D.tsx       # 3D animated background
│   │   │   ├── SchemaVisualizer3D.tsx # 3D database schema
│   │   │   ├── QueryInput.tsx         # Query input with voice
│   │   │   └── ResultsDisplay.tsx     # Results with charts
│   │   │
│   │   ├── 📁 pages/                   # Page Components
│   │   │   └── Dashboard.tsx          # Main dashboard page
│   │   │
│   │   ├── 📁 services/                # API Services
│   │   │   └── api.ts                 # API client
│   │   │
│   │   ├── 📁 store/                   # State Management
│   │   │   └── index.ts               # Zustand store
│   │   │
│   │   ├── 📁 types/                   # TypeScript Types
│   │   │   └── index.ts               # Type definitions
│   │   │
│   │   ├── App.tsx                     # Root component
│   │   ├── main.tsx                    # Entry point
│   │   └── index.css                   # Global styles
│   │
│   ├── index.html                      # HTML template
│   ├── package.json                    # Node dependencies
│   ├── vite.config.ts                  # Vite configuration
│   ├── tsconfig.json                   # TypeScript config
│   ├── tailwind.config.js              # Tailwind CSS config
│   ├── postcss.config.js               # PostCSS config
│   └── Dockerfile                      # Docker image definition
│
├── docker-compose.yml                   # Docker orchestration
├── setup.sh                             # Setup automation script
├── .gitignore                           # Git ignore rules
├── README.md                            # Main documentation
└── QUICKSTART.md                        # Quick start guide
```

## Key Files Explained

### Backend

#### `main.py`
- FastAPI application initialization
- CORS middleware configuration
- Route inclusion
- Startup/shutdown events

#### `app/core/config.py`
- Environment variables management
- Application settings
- Database URLs
- API keys configuration

#### `app/db/database.py`
- SQLAlchemy engine setup
- Database session management
- Schema inspection utilities
- Connection pooling

#### `app/services/ai_service.py`
- Claude AI integration
- Natural language to SQL conversion
- Insight generation
- SQL explanation

#### `app/services/query_service.py`
- SQL query execution
- Safety validation
- Complexity analysis
- Query optimization

#### `app/api/query_routes.py`
- `/query` - Execute natural language query
- `/databases/{id}/schema` - Get database schema
- `/databases/{id}/tables/{name}/sample` - Get sample data
- `/queries/history` - Query history
- `/databases` - Database management

### Frontend

#### `src/App.tsx`
- React Router setup
- QueryClient configuration
- Root component

#### `src/components/Background3D.tsx`
- Three.js particle system
- Animated data sphere
- 3D canvas setup

#### `src/components/SchemaVisualizer3D.tsx`
- Interactive 3D schema visualization
- Table nodes with metadata
- Relationship lines
- Orbit controls

#### `src/components/QueryInput.tsx`
- Natural language input
- Voice recognition
- Auto-resize textarea
- Quick suggestions

#### `src/components/ResultsDisplay.tsx`
- Data table view
- Multiple chart types (bar, line, pie)
- SQL code display
- AI insights panel
- CSV export

#### `src/services/api.ts`
- Axios client setup
- API endpoint methods
- Request/response interceptors
- Error handling

#### `src/store/index.ts`
- Zustand state management
- Database selection
- Query history
- UI state (sidebar, theme)

## Data Flow

```
User Input (Natural Language)
    ↓
QueryInput Component
    ↓
API Service (POST /api/v1/query)
    ↓
Query Routes Handler
    ↓
AI Service (Claude API)
    ↓
Generate SQL
    ↓
Query Service (Execute SQL)
    ↓
Database Query Execution
    ↓
AI Service (Generate Insights)
    ↓
Response with Results + Insights
    ↓
ResultsDisplay Component
    ↓
User sees: Table, Charts, Insights
```

## Technology Stack

### Backend
- **Framework**: FastAPI 0.109.0
- **Database ORM**: SQLAlchemy 2.0
- **AI**: Anthropic Claude API
- **Vector DB**: ChromaDB
- **Cache**: Redis
- **Task Queue**: Celery
- **Validation**: Pydantic 2.0

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite 5
- **Language**: TypeScript 5
- **3D Graphics**: Three.js + React Three Fiber
- **Animation**: Framer Motion
- **Charts**: Recharts
- **State**: Zustand
- **HTTP**: Axios + TanStack Query
- **Styling**: Tailwind CSS 3

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Databases**: PostgreSQL, MongoDB, Redis
- **Reverse Proxy**: Nginx (production)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/query` | Execute NL query |
| GET | `/api/v1/databases` | List databases |
| POST | `/api/v1/databases` | Create database |
| GET | `/api/v1/databases/{id}/schema` | Get schema |
| GET | `/api/v1/databases/{id}/tables/{name}/sample` | Sample data |
| GET | `/api/v1/queries/history` | Query history |
| GET | `/health` | Health check |

## Environment Variables

### Required
- `ANTHROPIC_API_KEY` - Claude API key
- `DATABASE_URL` - PostgreSQL connection
- `SECRET_KEY` - JWT secret

### Optional
- `REDIS_URL` - Redis connection
- `MONGODB_URL` - MongoDB connection
- `ALLOWED_ORIGINS` - CORS origins
- `DEBUG` - Debug mode
- `MAX_QUERY_COMPLEXITY` - Query limits

## Development Workflow

1. **Make changes** to code
2. **Hot reload** automatically applies changes
3. **Test** with sample queries
4. **Check logs** with `docker-compose logs -f`
5. **Commit** changes
6. **Build** for production with `npm run build`

## Production Deployment

1. Set `DEBUG=False`
2. Configure production database
3. Set secure `SECRET_KEY`
4. Configure CORS origins
5. Use production Docker Compose
6. Set up reverse proxy (Nginx)
7. Enable HTTPS
8. Configure monitoring

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.
