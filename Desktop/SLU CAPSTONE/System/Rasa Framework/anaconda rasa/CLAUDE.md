# Grace Church Chatbot — Rasa Framework

## Project Overview
This is the **SLU Capstone** project: a Rasa-based chatbot for **Grace Church**. It uses a hybrid architecture — a real Rasa NLU/Core model for training/intent classification, plus a custom Flask API server (`grace_api.py`) as a fallback on Windows (bypasses Rasa's tar extraction issues).

The chatbot answers questions about the church's mission, vision, and general inquiries. Dynamic content (mission, vision) is fetched live from a **Supabase** backend.

---

## Architecture

```
grace_chatbot.html  ←→  Flask API (grace_api.py :8000)
                              ↓
                        database.py (Supabase)
                              ↓
                    site_settings table (key=about)

Rasa pipeline (separate):
  rasa train → models/
  rasa run actions → action_endpoint :5055
  rasa shell / rasa run → :5005
```

### Key Files
| File | Purpose |
|------|---------|
| `grace_api.py` | Custom Flask server (primary entry point on Windows) |
| `database.py` | Supabase client + `SiteSettings` / `ChurchInfo` models |
| `actions/actions.py` | Rasa custom actions (`action_get_mission`, `action_get_vision`) |
| `domain.yml` | Rasa domain — intents, responses, actions |
| `config.yml` | Rasa NLU pipeline (DIETClassifier, FallbackClassifier) + policies |
| `data/nlu.yml` | NLU training examples |
| `data/stories.yml` | Conversation stories |
| `data/rules.yml` | Rasa rules |
| `endpoints.yml` | Action server endpoint (`http://localhost:5055/webhook`) |
| `grace_chatbot.html` | Frontend chat UI |
| `admin.py` | Admin utilities |
| `seed.py` | Database seeding script |
| `migrate.py` | Database migration script |

---

## Running the Project

### Option A: Custom Flask API (Windows-friendly)
```bash
pip install -r requirements_db.txt
python grace_api.py
# Server at http://localhost:8000
# Webhook: http://localhost:8000/webhooks/rest/webhook
```

### Option B: Full Rasa Stack
```bash
# Terminal 1 — train model (first time or after data changes)
rasa train

# Terminal 2 — run action server
rasa run actions

# Terminal 3 — run Rasa server
rasa run --enable-api --cors "*"
```

---

## Database (Supabase)
- **Backend**: Supabase (PostgreSQL)
- **Primary table**: `site_settings` — key/value store, `key='about'` holds a JSON object with `mission` and `vision` fields
- **Legacy table**: `church_info` — kept for backwards compatibility via `ChurchInfo` class
- Config is in `database.py` (`SUPABASE_URL`, `SUPABASE_KEY`)

---

## Intents
| Intent | Description |
|--------|-------------|
| `greet` | User greeting |
| `goodbye` | Farewell |
| `affirm` / `deny` | Yes/No responses |
| `mood_great` / `mood_unhappy` | Mood check-in |
| `bot_challenge` | Is this a bot? |
| `ask_mission` | Church mission query |
| `ask_vision` | Church vision query |

---

## Dependencies
- **Rasa** 3.x (NLU + Core)
- **rasa-sdk** (custom actions)
- **Flask** 2.3.2 + **flask-cors** (custom API server)
- **supabase** >=2.0.0 (database client)

Install extras: `pip install -r requirements_db.txt`

---

## Notes
- The `grace_api.py` uses simple keyword-based intent classification (not Rasa NLU) — it's a lightweight fallback
- The `FallbackClassifier` threshold is `0.3` — adjust in `config.yml` if too many messages fall through
- Models are saved in `models/` — retrain with `rasa train` after changing `data/` or `domain.yml`
- `ChurchInfo` class is legacy and delegates to `SiteSettings` internally
