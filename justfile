#!/usr/bin/env -S just --justfile
# ^ A shebang isn't required, but allows a justfile to be executed
#   like a script, with `./justfile test`, for example.

# List all available commands
@default:
    just --list

# Install dependencies using uv
@install:
    uv pip sync --system pyproject.toml

# Install dev dependencies
@install-dev:
    uv pip install --system ruff bandit

# Run the application
@run:
    streamlit run chatbot.py

# Run code linting with ruff
@lint:
    ruff check .

# Run security scanning with bandit
@security-scan:
    bandit -r .

# Format code using ruff
@format:
    ruff format .

# Run all checks (lint + security)
@check: lint security-scan

# Build Docker image
@build:
    docker build -t studentwhisperer:latest .

# Run Docker container (default port: 8501, can be overridden)
@docker-run port="8501":
    docker run -p {{port}}:80 --env-file .env studentwhisperer:latest

# Create .env file from template
@setup-env:
    cp .env.sample .env
    @echo "Created .env file. Please fill in the required values."

# Create Streamlit secrets file from template
@setup-secrets:
    cp .streamlit/secrets.toml.sample .streamlit/secrets.toml
    @echo "Created secrets.toml file. Please fill in the required values."

# Clean Python cache files
@clean:
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type d -name "*.egg-info" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    find . -type d -name ".ruff_cache" -exec rm -rf {} +

# Deploy to Azure Container Apps (requires Azure CLI login)
@deploy:
    az acr login --name devopsstudentwhisperer
    docker tag studentwhisperer:latest devopsstudentwhisperer.azurecr.io/studentwhisperercontainer:latest
    docker push devopsstudentwhisperer.azurecr.io/studentwhisperercontainer:latest
    az containerapp up --name studentwhisperercontainer --resource-group devops-student-portal-app-rg --image devopsstudentwhisperer.azurecr.io/studentwhisperercontainer:latest

# Run complete setup (install deps + setup env files)
@setup: install setup-env setup-secrets
    @echo "Setup complete. Remember to fill in your .env and secrets.toml files."
