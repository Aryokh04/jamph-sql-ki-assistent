# This readme forms the basis of creating a one click installer for our KI assistant system. Please report any issues or missing steps.

# List of all repositories to clone for full setup:
   git clone https://github.com/PerErikGronvik/Jamph-Umami-Frontend 
   git clone https://github.com/PerErikGronvik/Jamph-Rag-Api-Umami.git
   git clone https://github.com/PerErikGronvik/Jamph-ML-Trainer
   git clone https://github.com/Mobin1738/Jamph-MLFlow Jamph-MLflow
# Not up yet
   git clone https://github.com/PerErikGronvik/Jamph-ML-Ollama
# For inspiration originals etc.
   git clone https://github.com/navikt/reops-ollama.git reops-ollama
      git clone https://github.com/eilifjohansen/umami-start-student #see instructions below
      #metabase see below.

# Tidligere instruksjoner er stort sett flyttet til mappen som den gjelder.

#Service ports overview for local development:
- Jamph-Ollama: http://localhost:11434
- MLFlow: http://localhost:5001
- Jamph-Postgress: http://localhost:8002
- Jamph-Rag-Api-Umami: http://localhost:8004 (Not implemented)
- Jamph-ML-Trainer: http://localhost:8003 (Not implemented)


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





# Start-Umami-Student and Metabase Modules
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