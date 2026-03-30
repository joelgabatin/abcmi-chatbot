# Open Chatbot Frontend

Open the Grace Church chatbot UI in the default browser.

```bash
start frontend/grace_chatbot.html
```

**Prerequisites:**
- The API server must be running first: `/start-api`
- The HTML file connects to `http://localhost:8000/webhooks/rest/webhook`

**Frontend file:** `frontend/grace_chatbot.html`

To test without the API server, open the file directly in a browser — it will show the UI but responses will fail until the server is running.
