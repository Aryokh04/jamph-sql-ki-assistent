# Module Installation Instructions

Instructions for installing optional modules or repositories.

## Student Umami

### Installation Steps
1. **Clone the repository**:
   git clone https://github.com/eilifjohansen/umami-start-student frontend/modules/umami-start-student

2. **Add the BigQuery key file**: 
   - Paste the file `fagtorsdag-prod-81a6-52ac69097f46.json` into the `frontend/modules/umami-start-student` folder. Keep the file secret, do not share it.

3. **Install and start**:
   cd frontend/modules/umami-start-student
   npm install (If first time)
   npm run start
   Click the link to continue
   

   Note: To restart the server, press `Ctrl+C` to stop it, then run `npm run start` again.