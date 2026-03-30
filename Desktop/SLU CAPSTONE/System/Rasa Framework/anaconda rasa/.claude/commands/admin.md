# Admin Panel

Launch the interactive admin panel to manage church content in Supabase.

```bash
conda run -n rasa310 python scripts/admin.py
```

**Menu options:**
- `[1]` View current mission & vision
- `[2]` Update mission text
- `[3]` Update vision text
- `[4]` View all church information
- `[5]` Reset to default values
- `[6]` Exit

**No model retraining needed** — content is fetched live from the database at query time.

For bulk database setup, use `/seed-db` instead.
