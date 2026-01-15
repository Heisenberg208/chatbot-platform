# Quick Start Guide

Get up and running with the Chatbot Platform in 5 minutes!

## 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/Heisenberg208/chatbot-platform.git
cd chatbot-platform

# Copy environment template
cp .env.example .env
```

## 2. Configure Environment

Edit `.env` file and add your API key:

```bash
# For Groq (FREE and FAST - Recommended!)
LLM_PROVIDER=groq
GROQ_API_KEY=gsk-your-key-here  # Get free key at https://console.groq.com/keys

# OR for OpenAI (paid)
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here

# OR for OpenRouter
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

## 3. Start Services

```bash
docker-compose up -d
```

Wait for services to start (about 30 seconds).

## 4. Test the API

```bash
# Check health
curl http://localhost:8000/health

# Run automated test
python test_api.py
```

## 5. Use the UI

```bash
# Install frontend dependencies
cd frontend
pip install -r requirements.txt
```
# Start Fronend
[Frontend Readme](frontend/README.md)


Open http://localhost:8501 in your browser.

## 6. Register and Chat

1. Go to the Register tab
2. Create an account with email and password
3. Login with your credentials
4. Create a new project
5. Add system prompts (optional)
6. Start chatting!

## Alternative: Local Development

If you prefer running without Docker:

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Start PostgreSQL (or use Docker)
docker run -d \
  --name postgres \
  -e POSTGRES_USER=chatbot \
  -e POSTGRES_PASSWORD=chatbot_password \
  -e POSTGRES_DB=chatbot_db \
  -p 5432:5432 \
  postgres:15-alpine

# Run migrations
cd backend
poetry run alembic upgrade head

# Start server
poetry run uvicorn app.main:app --reload
```

## Common Commands

```bash
# View logs
docker-compose logs -f backend

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Access database
docker-compose exec db psql -U chatbot -d chatbot_db
```

## Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart database
docker-compose restart db
```

### API Not Responding
```bash
# Check logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

### LLM Provider Errors
- Verify your API key is correct in `.env`
- Check if you have sufficient API credits
- Ensure `LLM_PROVIDER` matches your API key type

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the API at http://localhost:8000/docs
- Customize system prompts for your use case
- Build a custom frontend using the API

## Support

- GitHub Issues: [repository]/issues
- Documentation: README.md
- API Docs: http://localhost:8000/docs
