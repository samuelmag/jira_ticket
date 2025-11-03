# 🧩 Jira Ticket Creator (GitHub → Jira)

Lightweight Flask service that listens for GitHub issue comment webhooks and automatically creates a Jira issue when a comment contains the command `/jira`.

---

## 🚀 What This Project Does

- Listens for GitHub webhook events (`X-GitHub-Event: issue_comment`).
- When a comment body equals `/jira` (case-insensitive), it creates an issue in Jira using the **Jira REST API**.
- Logs requests to the console for debugging and traceability.

Main logic lives in **`test.py`** (function `createJIRA`).

---

## 📂 Files

| File | Description |
|------|--------------|
| `test.py` | Main Flask app and webhook handler |

---

## 🧰 Prerequisites

- Python **3.8+**
- Jira Cloud account with API token

---

## ⚙️ Environment Variables

Set these before running the app:

| Variable | Description |
|-----------|--------------|
| `JIRA_URL` | Base URL for your Jira instance (e.g. `https://yourcompany.atlassian.net`) |
| `JIRA_API_TOKEN` | API token for your Jira account |
| `JIRA_EMAIL` | Jira account email |

Example (PowerShell):

```powershell
$env:JIRA_URL = "https://yourcompany.atlassian.net"
$env:JIRA_API_TOKEN = "your_api_token"
$env:JIRA_EMAIL = "you@example.com"
```

---

## 🧑‍💻 Installation

```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

pip install --upgrade pip
pip install flask requests
```

Or with `requirements.txt`:

```
flask
requests
```

Then:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run (Development)

```bash
python test.py
```

By default, the app listens on:  
`http://0.0.0.0:5000`  

For production, use a proper WSGI server (e.g. **gunicorn** or **uwsgi**) and secure your credentials.

---

## 🔗 Endpoint

### `POST /createJIRA`
- Expects a GitHub webhook payload.
- Requires the header: `X-GitHub-Event: issue_comment`.
- Triggers **only** when the comment body equals `/jira`.

#### Example test (local):

```bash
curl -X POST http://localhost:5000/createJIRA   -H "Content-Type: application/json"   -H "X-GitHub-Event: issue_comment"   -d '{"comment": {"body": "/jira", "user": {"login": "octocat"}}, "issue": {"html_url": "https://github.com/org/repo/issues/123"}}'
```

---

## 🧠 Architecture Overview

```mermaid
flowchart LR
    A[GitHub Issue Comment Event] -->|Webhook Payload| B[Flask App /createJIRA]
    B -->|POST JSON to Jira API| C[Jira Cloud]
    C -->|Response (201)| B
    B -->|Return Status| D[GitHub Webhook Delivery Log]
```

---

## 🧩 Recent Fixes & Improvements

| Change | Description |
|--------|--------------|
| ✅ Added flexible JSON parsing | Handles missing `comment` or `issue` keys safely |
| ✅ Console logging added | Prints payload and event info to help debug |
| ✅ Dynamic checks | Validates trigger comment `/jira` before creating issues |
| ✅ Cleaned payload structure | Jira issue summary, description, and user info formatted clearly |
| ✅ Error responses improved | 400 errors now return clear messages |

---

## 🔒 Security & Best Practices

- **Do not** expose your Flask debug server publicly.
- Validate GitHub webhook signatures (HMAC) before trusting payloads.
- Use **AWS Secrets Manager** or `.env` files for environment variables.
- Use HTTPS and firewall rules to limit access to port 5000.

---

## 🧱 Future Enhancements

- ✅ Configurable project key and issue type via environment vars.
- 🧪 Unit tests for webhook handler and Jira API integration.
- 🔐 Add webhook signature validation.

---

## 📜 License

Add an appropriate license file if you intend to open-source this project.

---

## 💡 Credits

Developed by **Magunda Samuel** — integrating GitHub automation with Jira using Flask on AWS EC2.
