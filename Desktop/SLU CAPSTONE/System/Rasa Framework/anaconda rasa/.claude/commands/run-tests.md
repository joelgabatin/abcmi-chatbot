# Run Tests

Run the chatbot test suite.

```bash
conda run -n rasa310 python test_grace_bot.py
```

Or run Rasa's built-in tests (requires trained model):

```bash
conda run -n rasa310 rasa test
```

Test files are located in `tests/`.
