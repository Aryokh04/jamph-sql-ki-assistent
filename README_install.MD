## This readme forms the basis of creating a one click installer for our KI assistant system. Please report any issues or missing steps. After the project is finsished expect this readme to change to be a full local install. to show of your work.

#Linker
## List of all repositories to clone for full setup:
   git clone https://github.com/navikt/Jamph-Umami-Frontend.git <br>
   git clone https://github.com/navikt/Reops-Jamph-Rag-Api-Umami.git<br>
   git clone https://github.com/navikt/Reops-Jamph-Ollama.git
## Depricated, old local versions, will be relevant again after bcs is done.
   git clone https://github.com/PerErikGronvik/Jamph-Umami-Frontend <br>
   git clone https://github.com/PerErikGronvik/Jamph-Rag-Api-Umami.git <br>
   git clone https://github.com/PerErikGronvik/Jamph-Ollama
## List of optional repositories
   git clone https://github.com/PerErikGronvik/Jamph-ML-Trainer
## only if time for it repositories that is cut from the project scope but could be interesting for the future:
   git clone https://github.com/Mobin1738/Jamph-MLFlow <br>
   git clone https://github.com/PerErikGronvik/Jamph-Postgres
## For inspiration originals etc.
   git clone https://github.com/navikt/reops-ollama.git reops-ollama <br>
   git clone https://github.com/eilifjohansen/umami-start-student #see instructions below
   #metabase see below.

# API CALLS
## Api linker på NAIS. her når du tjenestene som er i produksjon på NAIS. 

- **Jamph Frontend**: https://jamph.ekstern.dev.nav.no/ <br>
- **Jamph RAG API**: https://jamph-rag-api-umami.ekstern.dev.nav.no/  <br>
- **Jamph Ollama**: https://jamph-ollama.ekstern.dev.nav.no/

## ikke aktuelle
- **MLFlow**: https://jamph-mlflow.researchops.nav.no <br>
- **PostgreSQL**: Ikke påbegynt


# Disse instruksjonene vil bli relevante etter bcs slutt. ignorer.

## Service ports overview for local development:
- Jamph-Ollama: http://localhost:11434 <br>
- MLFlow: http://localhost:5001 <br>
- Jamph-Postgress: http://localhost:8002 <br>
- Jamph-Rag-Api-Umami: http://localhost:8004 (Not implemented) <br>
- Jamph-ML-Trainer: http://localhost:8003 (Not implemented)



# Dette er for nyskjerrige sjeler

# Start-Umami-Student and Metabase Modules
## A Backup of the original - Start-Umami-Student Module (To download UMAMI Student edition and run it locally)
**This is the original for reference**
   git clone https://github.com/eilifjohansen/umami-start-student Start-Umami-Student_original <br>
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