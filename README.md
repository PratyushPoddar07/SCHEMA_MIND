# QueryMind AI - Natural Language to SQL Platform

![QueryMind AI](https://img.shields.io/badge/AI-Powered-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green)
![React](https://img.shields.io/badge/React-18.2.0-blue)
![Three.js](https://img.shields.io/badge/Three.js-3D-orange)

A cutting-edge platform that transforms natural language questions into SQL queries, executes them, and provides AI-powered insights with stunning 3D visualizations.

## 🌟 Features

### Core Capabilities
- **Natural Language Processing**: Ask questions in plain English
- **Multi-Database Support**: PostgreSQL, MySQL, MongoDB, SQLite
- **AI-Powered Insights**: Automatic pattern detection, trend analysis, anomaly detection
- **SQL Explanation**: Learn SQL as you query
- **3D Schema Visualization**: Interactive 3D representation of your database structure
- **Voice Input**: Speak your queries naturally
- **Conversational Context**: Follow-up questions with memory
- **Query Optimization**: Automatic performance suggestions

### Advanced Features
- **Real-time Results**: Instant query execution with progress tracking
- **Multiple Visualizations**: Tables, bar charts, line charts, pie charts, 3D scatter plots
- **Export Capabilities**: Download results as CSV
- **Query Templates**: Save and reuse common queries
- **Query History**: Track all your queries with full context
- **Schema Caching**: Fast schema inspection and autocomplete

### UI/UX Excellence
- **3D Animated Background**: Beautiful particle effects
- **Glass Morphism Design**: Modern, sleek interface
- **Smooth Animations**: Framer Motion powered transitions
- **Responsive Design**: Works on all devices
- **Dark Mode**: Eye-friendly interface
- **Real-time Feedback**: Loading states, error handling, success notifications

## 🏗️ Architecture

```
querymind-ai/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Config & security
│   │   ├── db/             # Database connections
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   │   ├── ai_service.py      # Claude AI integration
│   │   │   └── query_service.py   # Query execution
│   │   └── utils/          # Utilities
│   ├── main.py            # FastAPI app
│   └── requirements.txt
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   │   ├── Background3D.tsx
│   │   │   ├── SchemaVisualizer3D.tsx
│   │   │   ├── QueryInput.tsx
│   │   │   └── ResultsDisplay.tsx
│   │   ├── pages/         # Page components
│   │   ├── services/      # API clients
│   │   ├── store/         # State management (Zustand)
│   │   └── types/         # TypeScript types
│   └── package.json
│
└── docker-compose.yml     # Docker orchestration
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)
- Anthropic API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/querymind-ai.git
cd querymind-ai
```

2. **Set up environment variables**
```bash
# Create .env file in root directory
cat > .env << EOF
ANTHROPIC_API_KEY=your_anthropic_api_key_here
SECRET_KEY=$(openssl rand -hex 32)
EOF
```

3. **Start with Docker Compose**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs

### Manual Setup (Without Docker)

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 📚 Usage Guide

### Connecting a Database

1. Navigate to the dashboard
2. Click on "Add Database" in the sidebar
3. Fill in the connection details:
   - **Name**: Friendly name for your database
   - **Type**: PostgreSQL, MySQL, MongoDB, or SQLite
   - **Connection String**: Database URL
   
   Example PostgreSQL:
   ```
   postgresql://user:password@localhost:5432/dbname
   ```

4. Click "Test Connection" then "Save"

### Asking Questions

Simply type or speak your question in natural language:

```
"Show me all customers who made purchases last month"
"What are the top 10 products by revenue?"
"Count orders grouped by status"
"Find users who haven't logged in for 30 days"
```

### Understanding Results

QueryMind AI provides:
1. **Generated SQL**: See the exact query that was generated
2. **Results Table**: View your data in a clean table
3. **Visualizations**: Auto-suggested charts based on your data
4. **AI Insights**: Patterns, trends, and anomalies detected
5. **Performance Metrics**: Query execution time

### 3D Schema Visualizer

Click the schema button to see:
- Interactive 3D representation of tables
- Visual relationships between tables
- Click tables to see column details
- Zoom, pan, and rotate the view

## 🔧 Configuration

### Backend Configuration

Edit `backend/.env`:

```env
# Application
APP_NAME=QueryMind AI
DEBUG=True

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/querymind

# AI
ANTHROPIC_API_KEY=your_key_here

# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Query Settings
MAX_QUERY_COMPLEXITY=10
QUERY_TIMEOUT_SECONDS=30
```

### Frontend Configuration

Edit `frontend/vite.config.ts` to change proxy settings or ports.

## 🎨 Customization

### Adding New Visualizations

1. Create a new component in `frontend/src/components/visualizations/`
2. Import recharts or Three.js components
3. Add to the view mode selector in `ResultsDisplay.tsx`

### Adding New Database Types

1. Add database driver to `backend/requirements.txt`
2. Update `DatabaseType` enum in `schemas.py`
3. Add connection logic in `database.py`
4. Update schema inspector for the new database

### Customizing AI Behavior

Edit `backend/app/services/ai_service.py`:
- Modify prompts for different SQL generation styles
- Adjust insight generation logic
- Change confidence thresholds

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app tests/
```

### Frontend Tests
```bash
cd frontend
npm run test
npm run test:coverage
```

## 📊 API Documentation

### Query Endpoint
```http
POST /api/v1/query
Content-Type: application/json

{
  "natural_language_query": "Show me all users",
  "database_id": 1,
  "include_insights": true,
  "explain_sql": true
}
```

### Response
```json
{
  "id": 1,
  "natural_language_query": "Show me all users",
  "generated_sql": "SELECT * FROM users LIMIT 1000",
  "execution_time_ms": 45,
  "result_count": 150,
  "status": "success",
  "results": [...],
  "insights": {...},
  "sql_explanation": "This query retrieves all records...",
  "visualization_suggestions": ["table", "bar_chart"]
}
```

## 🔒 Security

- SQL injection prevention through query validation
- Read-only query execution (no INSERT, UPDATE, DELETE)
- Connection string encryption
- Rate limiting on API endpoints
- CORS configuration
- JWT authentication (optional)

## 🚀 Deployment

### Production Build

#### Backend
```bash
cd backend
pip install -r requirements.txt
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

#### Frontend
```bash
cd frontend
npm run build
# Serve the dist/ folder with nginx or similar
```

### Docker Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables for Production
```env
DEBUG=False
ALLOWED_ORIGINS=https://yourdomain.com
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Anthropic Claude](https://anthropic.com) - AI-powered SQL generation
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - UI framework
- [Three.js](https://threejs.org/) - 3D graphics
- [Recharts](https://recharts.org/) - Data visualization

## 📧 Support

- Documentation: [docs.querymind.ai](https://docs.querymind.ai)
- Issues: [GitHub Issues](https://github.com/yourusername/querymind-ai/issues)
- Email: support@querymind.ai

## 🗺️ Roadmap

- [ ] Natural language to NoSQL (MongoDB queries)
- [ ] Multi-step query chains
- [ ] Real-time collaboration
- [ ] Query performance analytics dashboard
- [ ] Custom AI model fine-tuning
- [ ] Integration with BI tools
- [ ] Mobile app (iOS/Android)
- [ ] Voice-only mode
- [ ] Advanced 3D data visualizations

---

Made with ❤️ by the QueryMind Team
