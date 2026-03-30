# Check Database Health

Test the Supabase database connection and verify all required tables are accessible.

Read `database.py` and then run a quick connectivity check:

```bash
conda run -n rasa310 python -c "
import sys, os
sys.path.insert(0, os.getcwd())
from database import Database, SiteSettings, ChurchHistory, ChurchBranch, Pastor
db = Database()
ok = db.connect()
print('Connection:', 'OK' if ok else 'FAILED')
if ok:
    print('site_settings:', SiteSettings.get_about(db) is not None)
    print('branches:', len(ChurchBranch.get_all_regions(db) or []), 'regions')
    print('pastors:', len(Pastor.get_all_with_branches(db) or []), 'pastors')
    db.disconnect()
"
```

**Expected output when healthy:**
```
Connection: OK
site_settings: True
branches: N regions
pastors: N pastors
```

For a deeper check including table verification, use `/migrate`.
