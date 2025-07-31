# PurpleAir Sensor Dashboard

This dashboard displays the status of PurpleAir sensors using Flask.

## Files
- app.py: Flask app
- templates/dashboard.html: HTML template
- cleaned_sensor_data.csv: Cleaned sensor data
- requirements.txt: Python dependencies

## Deploy on Render (Free Hosting)

1. Go to https://render.com/
2. Create a free account and click "New Web Service"
3. Choose "Deploy from GitHub" or "Manual Deploy"
4. If using GitHub:
   - Push these files to a GitHub repository
   - Connect your GitHub account to Render
   - Select the repo and deploy
5. If uploading manually:
   - Zip this folder and upload it to Render
6. Set the following:
   - Build Command: pip install -r requirements.txt
   - Start Command: python app.py
