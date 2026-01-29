# Frontend Installation Instructions

## Student Umami Module (To download UMAMI Student edition and run it locally)
**This is the original for reference**
   umami-start-student
   - Paste the file `fagtorsdag-prod-81a6-52ac69097f46.json` into the `frontend/umami-start-student` folder. Keep the file secret, do not share it.

**Install and start**:
   cd frontend
   npm install (If first time)
   npm run start
   Click the link to continue
   
   Note: To restart the server, press `Ctrl+C` to stop it, then run `npm run start` again.

# Backend Installation Instructions

git clone https://github.com/PerErikGronvik/JAMPH-SQL-ki-assistent-backend backend

# Module Installation Instructions

Instructions for installing optional modules or repositories.

## Student Umami Module (To download UMAMI Student edition and run it locally)
**This is the original for reference**
   git clone https://github.com/eilifjohansen/umami-start-student frontend/modules/umami-start-student
   - Paste the file `fagtorsdag-prod-81a6-52ac69097f46.json` into the `frontend/modules/umami-start-student` folder. Keep the file secret, do not share it.

**Install and start**:
   cd frontend/modules/umami-start-student
   npm install (If first time)
   npm run start
   Click the link to continue
   

   Note: To restart the server, press `Ctrl+C` to stop it, then run `npm run start` again.

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
   git clone --depth 1 https://github.com/metabase/metabase.git frontend/modules/metabase
   Source: https://github.com/metabase/metabase

# For backend modules look in the backend/README_install.MD