# Seed the Database

Populate the Supabase database with default church content.

```bash
conda run -n rasa310 python scripts/seed.py
```

Run this once during initial setup or to reset the database to default values.

For targeted content updates, use `/update-content` (`scripts/admin.py`) instead.
