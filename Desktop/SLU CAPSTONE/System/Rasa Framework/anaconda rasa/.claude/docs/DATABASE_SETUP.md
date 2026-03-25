# Grace Church Chatbot - Database Setup Guide

## Prerequisites

You need MySQL Server installed and running. Download from: https://www.mysql.com/downloads/

## Setup Steps

### Step 1: Install Database Dependencies

```powershell
conda run -n rasa310 pip install mysql-connector-python
```

### Step 2: Configure Database Credentials

Edit `database.py` and update these settings:

```python
DB_CONFIG = {
    "host": "localhost",      # MySQL server host
    "user": "root",           # MySQL username
    "password": "",           # MySQL password (empty by default)
    "database": "grace_church_chatbot",
    "port": 3306
}
```

### Step 3: Run Database Migration

This creates the `church_info` table:

```powershell
conda run -n rasa310 python migrate.py
```

Expected output:
```
✓ Database 'grace_church_chatbot' created/verified
✓ church_info table created/verified
✅ Migration completed successfully!
```

### Step 4: Seed the Database

This populates the database with mission and vision:

```powershell
conda run -n rasa310 python seed.py
```

Expected output:
```
✓ Connected to database
✓ Cleared existing data
✓ Mission inserted successfully
✓ Vision inserted successfully
📌 MISSION: Our mission at Grace Church...
📌 VISION: Our vision is to be a thriving...
✅ Seeding completed successfully!
```

### Step 5: Start the Chatbot API

```powershell
conda run -n rasa310 python grace_api.py
```

The API will be running at: `http://localhost:8000`

## Testing the API

### Health Check
```powershell
Invoke-WebRequest http://localhost:8000/health | ConvertFrom-Json
```

### Chat Request
```powershell
$body = @{sender="user"; message="What is the mission?"} | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:8000/webhooks/rest/webhook" `
  -Method POST -ContentType "application/json" -Body $body | ConvertFrom-Json
```

### Web Interface
Open: `grace_chatbot.html`

## Database Structure

### church_info Table
- `id` - Primary key
- `type` - VARCHAR(50) - Type of info ('mission', 'vision', etc.)
- `content` - LONGTEXT - The actual content
- `created_at` - TIMESTAMP - When created
- `updated_at` - TIMESTAMP - Last update

## Updating Church Information

To update mission or vision in the database:

```powershell
# Use MySQL command line
mysql -u root

# Then in MySQL:
USE grace_church_chatbot;
UPDATE church_info SET content = 'New mission text' WHERE type = 'mission';
```

Or re-run the seed script to reset to defaults.

## Troubleshooting

### "Error connecting to MySQL"
- Make sure MySQL Server is running
- Check hostname, username, and password in `database.py`
- Ensure the port is correct (default: 3306)

### "Table already exists"
- This is normal. The migration script uses `CREATE TABLE IF NOT EXISTS`

### Database not responding
- Check database connection in `grace_api.py` startup logs
- API will fall back to hardcoded responses if database is unavailable

## Files Overview

- `database.py` - Database connection and models
- `migrate.py` - Creates database schema
- `seed.py` - Populates database with initial data
- `grace_api.py` - Flask API server (updated to use database)
- `grace_chatbot.html` - Web interface for chatbot

Enjoy your Grace Church Chatbot! 🙏
