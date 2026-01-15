.PHONY: help install dev up down logs migration migrate test format lint clean

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies with Poetry
	poetry install

dev: ## Run development server
	cd backend && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

up: ## Start Docker services
	docker-compose up -d

down: ## Stop Docker services
	docker-compose down

logs: ## View Docker logs
	docker-compose logs -f backend

migration: ## Create a new migration
	@read -p "Enter migration message: " msg; \
	cd backend && poetry run alembic revision --autogenerate -m "$$msg"

migrate: ## Run pending migrations
	cd backend && poetry run alembic upgrade head

test: ## Run tests
	cd backend && poetry run pytest

format: ## Format code with Black
	poetry run black backend/

lint: ## Lint code with Ruff
	poetry run ruff check backend/

clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

frontend: ## Run Streamlit frontend
	cd frontend && streamlit run streamlit_app.py

db-shell: ## Access PostgreSQL shell
	docker-compose exec db psql -U chatbot -d chatbot_db

docker-build: ## Build Docker image
	docker build -t chatbot-platform:latest .

docker-run: ## Run Docker container
	docker run -d --name chatbot-api -p 8000:8000 chatbot-platform:latest

setup: ## Complete setup (install + migrate)
	$(MAKE) install
	$(MAKE) migrate
	@echo "Setup complete! Run 'make dev' to start the server."
