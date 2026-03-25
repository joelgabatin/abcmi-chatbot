# Retrain Rasa Model

Retrain the Rasa NLU + Core model after changes to `data/` or `domain.yml`.

```bash
conda run -n rasa310 rasa train
```

**When to retrain:**
- Added new intents in `data/nlu.yml`
- Added new stories/rules in `data/stories.yml` or `data/rules.yml`
- Changed `domain.yml` (intents, responses, actions)
- Changed `config.yml` (pipeline or policies)

**NOT needed for:**
- Updating mission/vision text (use `/update-content` instead)
- Changes to `grace_api.py` or `database.py`

After retraining, restart `grace_api.py` for changes to take effect.
