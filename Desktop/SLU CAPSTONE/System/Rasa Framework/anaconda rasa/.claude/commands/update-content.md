# Update Church Content (No Retraining)

Update mission, vision, or other church content stored in the Supabase database.

```bash
conda run -n rasa310 python admin.py
```

**Admin panel options:**
- `[1]` View mission & vision
- `[2]` Update mission text
- `[3]` Update vision text
- `[4]` View all information in database
- `[5]` Reset to default values
- `[6]` Exit

**No model retraining needed** — changes are live immediately since content is fetched from the database at query time.
