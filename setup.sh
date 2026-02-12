#!/bin/bash

# QueryMind AI Setup Script
echo "🚀 QueryMind AI Setup"
echo "===================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
ANTHROPIC_API_KEY=your_anthropic_api_key_here
SECRET_KEY=$(openssl rand -hex 32)
EOF
    echo "⚠️  Please edit .env file and add your Anthropic API key"
    read -p "Press enter to continue after updating .env..."
fi

# Create backend .env
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend/.env..."
    cp backend/.env.example backend/.env
fi

# Pull Docker images
echo "📦 Pulling Docker images..."
docker compose pull

# Build services
echo "🔨 Building services..."
docker compose build

# Start services
echo "🚀 Starting services..."
docker compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
docker compose ps

# Initialize database
echo "🗄️  Initializing database..."
docker compose exec backend alembic upgrade head 2>/dev/null || echo "⚠️  Database migrations will run on first API call"

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Access the application:"
echo "   Frontend:  http://localhost:5173"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/api/docs"
echo ""
echo "📚 View logs:"
echo "   docker compose logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker compose down"
echo ""
