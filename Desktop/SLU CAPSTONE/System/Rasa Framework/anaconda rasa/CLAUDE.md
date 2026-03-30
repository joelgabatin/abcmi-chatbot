# Grace Church Chatbot — Rasa Framework

## Project Overview
This is the **SLU Capstone** project: a Rasa-based chatbot for **Grace Church**. Flask (`grace_api.py`) acts as a thin gateway that proxies messages from the frontend to the Rasa server. All intent classification and response generation is handled by Rasa.

The chatbot answers questions about the church's mission, vision, history, branches, pastors, and more. Dynamic content is fetched live from a **Supabase** backend via Rasa custom actions.

---

## Architecture

```
Frontend (:8000)
    ↓
Flask gateway — grace_api.py (:8000)   [CORS, proxying only]
    ↓
Rasa server (:5005)                    [NLU intent classification + Core policies]
    ↓
Rasa action server (:5055)             [Custom actions — database queries]
    ↓
Supabase (PostgreSQL)
```

### Key Files
| File | Purpose |
|------|---------|
| `grace_api.py` | Flask gateway — proxies requests to Rasa, handles CORS |
| `database.py` | Supabase client + all database model classes |
| `actions/actions.py` | Rasa custom actions (query Supabase, build responses) |
| `actions/about_church/` | Modular actions for mission, vision, history, beliefs, etc. |
| `actions/branches/` | Modular actions for branch queries |
| `actions/pastors/` | Modular actions for pastor queries |
| `domain.yml` | Rasa domain — intents, entities, slots, responses, actions |
| `config.yml` | Rasa NLU pipeline (DIETClassifier, FallbackClassifier) + policies |
| `data/nlu/` | NLU training examples |
| `data/stories/` | Conversation stories |
| `data/rules/` | Rasa rules |
| `endpoints.yml` | Action server endpoint (`http://localhost:5055/webhook`) |
| `frontend/grace_chatbot.html` | Frontend chat UI |

---

## Running the Project

```bash
# Terminal 1 — train model (first time or after data/domain changes)
rasa train --domain domain/

# Terminal 2 — run action server
rasa run actions

# Terminal 3 — run Rasa server (domain is already baked into the model)
rasa run --enable-api --cors "*"

# Terminal 4 — run Flask gateway (frontend connects here)
python grace_api.py
```

Frontend connects to `http://localhost:8000/webhooks/rest/webhook`.
Flask proxies the message to Rasa at `http://localhost:5005/webhooks/rest/webhook`.

---

## Database (Supabase)
- **Backend**: Supabase (PostgreSQL)
- **Primary table**: `site_settings` — key/value store for mission, vision, driving force
- **Other tables**: `church_history`, `statement_of_belief`, `church_core_values`, `church_branches`, `pastors`
- Config is in `database.py` (`SUPABASE_URL`, `SUPABASE_KEY`)

---

## Intents (defined in data/nlu/)
| Intent | Description |
|--------|-------------|
| `greet` | User greeting |
| `goodbye` | Farewell |
| `ask_mission` | Church mission query |
| `ask_vision` | Church vision query |
| `ask_history` | Church history query |
| `ask_statement_of_belief` | Beliefs/doctrine query |
| `ask_driving_force` | Driving force query |
| `ask_core_values` | Core values query |
| `ask_branches` | Branch finder (multi-turn) |
| `ask_total_branches` | Total branch count |
| `ask_local_branches` | Philippines branches |
| `ask_international_branches` | International branches |
| `ask_pastors` | List all pastors |
| `ask_specific_pastor` | Look up a specific pastor by name |
| `ask_pastor_branch_schedule` | Service schedule for a pastor's branch |

---

## Dependencies
- **Rasa** 3.x (NLU + Core)
- **rasa-sdk** (custom actions)
- **Flask** + **flask-cors** (gateway)
- **requests** (proxy calls from Flask to Rasa)
- **supabase** >=2.0.0 (database client)

Install: `pip install -r requirements_db.txt`

---

## Notes
- Flask is a **proxy only** — it does not classify intents or generate responses
- The `FallbackClassifier` threshold is `0.3` — adjust in `config.yml` if needed
- Retrain with `rasa train` after changing `data/` or `domain.yml`
- `ChurchInfo` class in `database.py` is legacy and delegates to `SiteSettings` internally
