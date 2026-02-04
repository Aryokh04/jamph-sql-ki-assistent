# This readme forms the basis of creating a one click installer for our KI assistant system. Please report any issues or missing steps.

# Frontend Installation Instructions

## Jamph-Umami-Frontend (Our version of Start-Umami-Student edition)
   git clone https://github.com/PerErikGronvik/Jamph-Umami-Frontend Jamph-Umami-Frontend
   - Paste the file `fagtorsdag-prod-81a6-52ac69097f46.json` into the `Jamph-Umami-Frontend` folder. Keep the file secret, do not share it.

**Install and start**:
   cd Jamph-Umami-Frontend
   npm install (If first time)
   npm run start
   Click the link to continue
   
   Note: To restart the server, press `Ctrl+C` to stop it, then run `npm run start` again.

## Jamph-Rag-Api-Umami (Backend RAG API)

This is our backend API for the KI assistant. It is called from the frontend and talks to Ollama and Database to assemble the RAG (Retrieval-Augmented Generation) system.

**Clone the repository**:
   ```bash
   git clone https://github.com/PerErikGronvik/JAMPH-SQL-ki-assistent-backend Jamph-Rag-Api-Umami
   ```

**Prerequisites**:
   - Python 3.11 or later (see Development setup.md)
   - UV package manager (see Development setup.md step 11)
   - Docker Desktop running (for Ollama and PostgreSQL dependencies)

**Install and start**:

**Windows (PowerShell):**
   ```powershell
   cd Jamph-Rag-Api-Umami
   
   # Install dependencies using UV (recommended)
   uv sync
   # Or using pip
   pip install -r requirements.txt
   
   # Set up environment variables
   copy example.env .env
   # Edit .env file with your configuration (use notepad or VS Code)
   
   # Start dependencies (Ollama and Database)
   cd ..
   docker compose up jamph-ollama jamph-db -d
   
   # Return to API directory and start the API
   cd Jamph-Rag-Api-Umami
   python main.py
   # Or with UV:
   uv run python main.py
   ```

**macOS:**
   ```bash
   cd Jamph-Rag-Api-Umami
   
   # Install dependencies using UV (recommended)
   uv sync
   # Or using pip
   pip3 install -r requirements.txt
   
   # Set up environment variables
   cp example.env .env
   # Edit .env file with your configuration (use nano, vim, or VS Code)
   
   # Start dependencies (Ollama and Database)
   cd ..
   docker compose up jamph-ollama jamph-db -d
   
   # Return to API directory and start the API
   cd Jamph-Rag-Api-Umami
   python3 main.py
   # Or with UV:
   uv run python3 main.py
   ```

**Linux:**
   ```bash
   cd Jamph-Rag-Api-Umami
   
   # Install dependencies using UV (recommended)
   uv sync
   # Or using pip
   pip3 install -r requirements.txt
   
   # Set up environment variables
   cp example.env .env
   # Edit .env file with your configuration (use nano, vim, or VS Code)
   
   # Start dependencies (Ollama and Database)
   cd ..
   docker compose up jamph-ollama jamph-db -d
   
   # Return to API directory and start the API
   cd Jamph-Rag-Api-Umami
   python3 main.py
   # Or with UV:
   uv run python3 main.py
   ```

**Environment variables to configure in .env file**:
   - `OLLAMA_HOST=http://localhost:11434`
   - `DB_HOST=localhost`
   - `DB_PORT=8002`
   - `DB_NAME=jamph_db`
   - `DB_USER=jamph`
   - `DB_PASSWORD=jamph_password`
   - `MLFLOW_TRACKING_URI=https://mlflow.vishvadukan.no`

**Verify installation**:
   - API should be running at http://localhost:8004
   - Check API health endpoint: http://localhost:8004/health (if available)
   - Check logs for any connection errors to Ollama or database

**Using Docker Compose** (alternative):
   ```bash
   # From project root
   docker compose up jamph-rag-api-umami -d
   ```
   Note: This will also start all dependencies (Ollama, database, MLFlow)

**To restart the API**:
   - Press `Ctrl+C` to stop the server
   - **Windows**: Run `python main.py` or `uv run python main.py` again
   - **macOS/Linux**: Run `python3 main.py` or `uv run python3 main.py` again


# Setup Instructions

# Module Installation Instructions

## Training Pipeline Module
   git clone https://github.com/PerErikGronvik/Jamph-ML-Trainer Jamph-ML-Trainer

## MLFlow Setup (Experiment Tracking & Model Registry)

**MLFlow is hosted centrally** - you don't need to install it locally. 

### Accessing MLFlow

**Authentication Required:**
   - MLFlow is protected with basic authentication
   - Get credentials from `mlflow.env` sent on email (keep secret!)

**Web Interface:**
   - Open in browser: https://mlflow.vishvadukan.no
   - Login with username and password from `mlflow.env`
   - View experiments, models, and metrics
  

**For local testing only** (optional):
   - Run MLFlow via Docker: `docker compose --profile mlflow up -d`
   - Access at http://localhost:5001
   - Note: Local instance won't share data with the team

**For Nav production deployment**:
   - Deploy MLFlow to Nav's internal infrastructure
   - Update `MLFLOW_TRACKING_URI` environment variable to point to Nav's server
   - All code remains the same - only the connection string changes

## Jamph-DB Setup (PostgreSQL Database)

**Jamph-DB is hosted centrally** - you don't need to install PostgreSQL locally.

**Development environment**: Connect to the shared database server
   - Set environment variables:
     - `DB_HOST=<server-address>`
     - `DB_PORT=5432`
     - `DB_NAME=jamph_db`
     - `DB_USER=jamph`
     - `DB_PASSWORD=<password>`
   - All team members connect to the same database instance to share data

**For local testing only** (optional):
   - Run PostgreSQL via Docker: `docker compose --profile jamph-db up -d`
   - Access at localhost:8002 (mapped to PostgreSQL port 5432)
   - Note: Local instance won't share data with the team

**For Nav production deployment**:
   - Deploy PostgreSQL to Nav's internal infrastructure
   - Update database environment variables to point to Nav's server
   - All code remains the same - only the connection details change


## Nav internal Ollama repo

git clone https://github.com/navikt/reops-ollama.git reops-ollama

## Docker Compose Services **in progress**

**Start all services**:
   docker compose --profile all up -d

**Start individual services**:
   docker compose --profile mlflow up -d

   docker compose --profile ollama up -d

   docker compose --profile jamph-rag-api-umami up -d
   
   docker compose --profile jamph-db up -d

   docker compose --profile jamph-ml-trainer up -d

**Service ports overview**:

- Jamph-Ollama: http://localhost:11434
- MLFlow: http://localhost:5001
- Jamph-DB: http://localhost:8002
- Jamph-Rag-Api-Umami: http://localhost:8004 (Not implemented)
- Jamph-ML-Trainer: http://localhost:8003 (Not implemented)


**Stop services**:
   docker compose down

   Note: To restart services, use `docker compose restart` or stop and start specific profiles.



# To install optional modules or repositories

Instructions for installing optional modules or repositories.

## A Backup of the original - Start-Umami-Student Module (To download UMAMI Student edition and run it locally)
**This is the original for reference**
   git clone https://github.com/eilifjohansen/umami-start-student Start-Umami-Student
   - Paste the file `fagtorsdag-prod-81a6-52ac69097f46.json` into the `Start-Umami-Student` folder. Keep the file secret, do not share it.

**Install and start**:
   
   Start-Umami-Student/npm install (If first time)
   Start-Umami-Student/npm run start
   Click the link to continue

   Note: To restart the server, press `Ctrl+C` to stop it, then run `Start-Umami-Student/npm run start` again.

## Metabase Module
**Start Docker Desktop first** - Make sure Docker Desktop is running before running any **docker commands**
docker pull metabase/metabase:latest (If first time)
docker run -d -p 3000:3000 --name metabase metabase/metabase (if first time)
docker start metabase (If metabase is already created and is not running, harmless if already running)
   - Open http://localhost:3000 in your browser
   - Click "Get started" and fill in the required information
   - You can skip most options and add data later in the interface

**Connect to BigQuery**
Download the BigQuery dataset file `fagtorsdag.json` from the email
In Metabase, go to **Data → Databases → Add database**
Select BigQuery and upload the JSON file with your credentials **keep the file secret **

**Optional - Clone Metabase source code for reference** (Warning: ~200-300 MB):
   git clone --depth 1 https://github.com/metabase/metabase.git Metabase
   Source: https://github.com/metabase/metabase

# For backend modules look in the backend/README_install.MD