# Sync NLU from Database

Sync `select_region` and `select_branch` NLU examples from Supabase into the NLU data files.

Run this whenever branches or regions change in the database, **before** retraining.

```bash
conda run -n rasa310 python scripts/sync_nlu.py
```

Then retrain:

```bash
conda run -n rasa310 rasa train
```

**What it does:**
- Reads all active regions and branches from Supabase
- Overwrites `select_region` and `select_branch` intent blocks in `data/nlu/branches/branches.yml`
- Preserves all other NLU content untouched
