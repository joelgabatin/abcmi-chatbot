# Grace Church Chatbot - Quick Database Setup

## ⚠️ Important: Start MySQL Server First!

### For Windows with MySQL Installed:

**Option 1: Using Services (Recommended)**
1. Press `Win + R`
2. Type: `services.msc`
3. Find "MySQL80" (or "MySQL57", "MySQL" depending on your version)
4. Right-click → Select "Start"
5. Wait for status to show "Running"

**Option 2: Using Command Line (As Administrator)**
```powershell
# Open PowerShell as Administrator, then:
net start MySQL80
```

**Option 3: Using MySQL Installer**
- Launch MySQL Installer
- Click "Server" → Reconfigure
- Choose the instance and start it

### Verify MySQL is Running:
```powershell
# Try connecting:
mysql -u root -p
# Press Enter if no password, otherwise enter your password
# Type: exit
```

---

## Database Setup Steps

Once MySQL is running, use the terminal in this directory and run:

### Step 1️⃣: Set Database Credentials
Edit `database.py` (around line 6):
```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",              # Your MySQL username
    "password": "",              # Your MySQL password (empty by default)
    "database": "grace_church_chatbot",
    "port": 3306
}
```

### Step 2️⃣: Create Database Schema
```powershell
conda run -n rasa310 python migrate.py
```

Expected output:
```
✓ Database 'grace_church_chatbot' created/verified
✓ church_info table created/verified
✅ Migration completed successfully!
```

### Step 3️⃣: Populate Database
```powershell
conda run -n rasa310 python seed.py
```

Expected output:
```
✓ Connected to database
✓ Cleared existing data
✓ Mission inserted successfully
✓ Vision inserted successfully
✅ Seeding completed successfully!
```

### Step 4️⃣: Start the Chatbot
```powershell
conda run -n rasa310 python grace_api.py
```

You should see:
```
✓ Database: Connected
✓ API will be available at: http://localhost:8000
```

### Step 5️⃣: Test It!
Open `grace_chatbot.html` in your browser or test with:
```powershell
Invoke-WebRequest http://localhost:8000/health | ConvertFrom-Json
```

---

## Created Files

✅ `database.py` - Database connection & models
✅ `migrate.py` - Schema creation script
✅ `seed.py` - Data population script
✅ `grace_api.py` - Updated API (now uses database)
✅ `requirements_db.txt` - Database dependencies
✅ `DATABASE_SETUP.md` - Detailed guide

---

## Commands Summary

```powershell
# 1. Start MySQL (if not running)
net start MySQL80

# 2. Migrate database
conda run -n rasa310 python migrate.py

# 3. Seed data
conda run -n rasa310 python seed.py

# 4. Start API
conda run -n rasa310 python grace_api.py

# 5. Open chatbot
start grace_chatbot.html
```

That's it! Your Grace chatbot is now database-connected! 🙏
