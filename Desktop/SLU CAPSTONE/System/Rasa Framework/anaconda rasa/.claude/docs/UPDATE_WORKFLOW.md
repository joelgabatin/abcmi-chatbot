# Grace Church Chatbot - Update Workflow Guide

## 🎯 Key Concept

**Rasa Model = Intent Recognition** (Does NOT store mission/vision content)
**MySQL Database = Content Storage** (Stores actual mission/vision text)

When user asks "What is the mission?" → Rasa recognizes intent → Database returns content.

---

## 📋 Workflow Comparison

### ✅ Updating Content (NO RETRAINING NEEDED)

**Scenario**: Church's mission statement changes

**Steps**:
```bash
# Run the admin panel
python admin.py

# Select option [2] to update mission
# Type new mission text
# Confirm

# That's it! Changes live immediately
# No model retraining needed
```

**Why?** The model only knows "user asked about mission", not what the mission IS.

---

### 🔄 Adding New Intents (RETRAINING REQUIRED)

**Scenario**: Want chatbot to handle questions like "What are your service times?"

**Steps**:
1. Add new intent to `data/nlu.yml`:
```yaml
- intent: ask_service_times
  examples: |
    - when do you meet?
    - what are your service times?
    - church hours?
```

2. Add response to `domain.yml`:
```yaml
responses:
  utter_service_times:
  - text: "Service times coming soon..."
```

3. Add story/rule to `data/stories.yml` or `data/rules.yml`

4. **Retrain the model**:
```bash
conda run -n rasa310 rasa train
```

5. **Add the data to database** (optional):
```bash
python admin.py
# Add service times info manually
```

---

## 🚀 Common Workflows

### Workflow 1: Simple Content Update

```
1. python admin.py
2. Select [2] or [3] for mission/vision
3. Enter new text
4. Done! (API queries DB automatically)
```

**Model retraining?** ❌ NO

---

### Workflow 2: Add New Feature (e.g., Events)

```
1. Edit data/nlu.yml (add ask_events intent)
2. Edit domain.yml (add utter_events response)
3. Edit data/rules.yml (add event rule)
4. conda run -n rasa310 rasa train (⚠️ RETRAIN)
5. python admin.py (add events to database)
6. Restart grace_api.py
```

**Model retraining?** ✅ YES

---

### Workflow 3: Change How Chatbot Recognizes Questions

```
1. Edit NLU examples in data/nlu.yml
2. conda run -n rasa310 rasa train (⚠️ RETRAIN)
3. Restart grace_api.py
```

**Model retraining?** ✅ YES

---

## 📊 Decision Tree

```
Did you change the mission/vision TEXT?
├─ YES → Use admin.py → NO retraining
└─ NO
   Did you add a NEW question type?
   ├─ YES → Update NLU + retrain → YES retraining
   └─ NO
      Did you change how chatbot recognizes questions?
      ├─ YES → Update NLU examples + retrain → YES retraining
      └─ NO → No action needed
```

---

## 🛠️ Admin Panel Usage

Run the admin panel:
```bash
python admin.py
```

**Options**:
- `[1]` View mission & vision
- `[2]` Update mission (text only)
- `[3]` Update vision (text only)
- `[4]` View all information in database
- `[5]` Reset to default values
- `[6]` Exit

Example:
```
Select option (1-6): 2
Current mission: Our mission at Grace Church...
Enter the new text (press Enter twice when done):
---
Our new mission is to serve with love
and empower our community

(Confirm? yes/no): yes
✅ Mission updated successfully!
```

---

## 🔄 Immediate vs Restart

| Action | Immediate? | Restart API? |
|--------|-----------|-------------|
| Update mission/vision with admin.py | ✅ Immediate | ❌ NO |
| Add new intent + retrain | ❌ Requires restart | ✅ YES |
| Change NLU examples + retrain | ❌ Requires restart | ✅ YES |

---

## ✨ Summary

```
✅ Don't retrain for CONTENT changes (mission/vision text)
✅ DO retrain for INTENT changes (new question types, recognition)
✅ Use admin.py to update content easily
✅ Always restart API after model retraining
```

Your architecture separates **concerns beautifully**:
- Rasa = Understanding (what the user is asking)
- Database = Knowledge (what to tell them)
- API = Logic (connecting the two)

This is how production chatbots work! 🚀
