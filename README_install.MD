# This readme forms the basis of creating a one click installer for our KI assistant system. Please report any issues or missing steps.

# Frontend Installation Instructions

## Jamph-Umami-Frontend (Our version of Start-Umami-Student edition)
   git clone https://github.com/PerErikGronvik/Jamph-Umami-Frontend Jamph-Umami-Frontend
   - Paste the file `fagtorsdag-prod-81a6-52ac69097f46.json` into the `Jamph-Umami-Frontend` folder. Keep the file secret, do not share it.

**Install and start**:
   Jamph-Umami-Frontend/npm install (If first time)
   Jamph-Umami-Frontend/npm run start
   Click the link to continue
   
   Note: To restart the server, press `Ctrl+C` to stop it, then run `Jamph-Umami-Frontend/npm run start` again.

# This is our backend API for the KI assistant, it is called from frontend and it talks to Ollama and Database and assembles the RAG system.

git clone https://github.com/PerErikGronvik/JAMPH-SQL-ki-assistent-backend Jamph-Rag-Api-Umami

**install instructions will be here**


# Setup Instructions

# Module Installation Instructions

## Training Pipeline Module
   git clone https://github.com/PerErikGronvik/Jamph-ML-Trainer Jamph-ML-Trainer

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