# Run Rasa Action Server

Start the Rasa custom action server (required for full Rasa stack mode).

```bash
conda run -n rasa310 rasa run actions
```

Runs on port **5055** — referenced in `endpoints.yml`.

**Use this when running the full Rasa stack (Option B), NOT when using `grace_api.py` (Option A).**

Full stack startup order:
1. `rasa run actions` (this command — Terminal 1)
2. `rasa run --enable-api --cors "*"` (Terminal 2)
