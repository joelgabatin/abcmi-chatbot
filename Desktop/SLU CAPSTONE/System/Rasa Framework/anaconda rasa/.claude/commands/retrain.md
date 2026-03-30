# Retrain Rasa Model

Retrain the Rasa NLU + Core model after changes to `data/` or `domain.yml`.

```bash
conda run -n rasa310 rasa train
```

**When to retrain:**
- Added or changed intents in `data/nlu/<feature>/<feature>.yml`
- Added or changed stories in `data/stories/<feature>/<feature>.yml`
- Added or changed rules in `data/rules/<feature>/<feature>.yml`
- Changed `domain.yml` (intents, responses, actions, slots)
- Changed `config.yml` (pipeline or policies)

**NOT needed for:**
- Updating mission/vision/content text (use `/update-content` instead)
- Changes to `grace_api.py` or `database.py`
- Changes to `actions/` code (action server picks these up on restart)

**Tip:** Run `/sync-nlu` first if branches or regions changed in the database.

After retraining, restart `grace_api.py` for changes to take effect.
