# Verify Database (Migrate)

Verify the Supabase connection and confirm required tables exist.

```bash
conda run -n rasa310 python scripts/migrate.py
```

**What it checks:**
1. Connects to Supabase using credentials in `database.py`
2. Verifies the `church_info` table is accessible
3. Reports row count and connection status

**Run this when:**
- Setting up the project for the first time
- Debugging a database connection error
- After changing `SUPABASE_URL` or `SUPABASE_KEY` in `database.py`

If the table is missing, create it in the Supabase SQL editor (SQL is shown in `scripts/migrate.py`).
