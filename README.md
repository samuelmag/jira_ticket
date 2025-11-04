<<<<<<< HEAD
# Jira Ticket Creator (GitHub → Jira)

Lightweight Flask service that listens for GitHub issue comment webhooks and creates a Jira issue when a comment contains the command `/jira`.

## What this project does

- Listens for GitHub webhook events (expects `X-GitHub-Event: issue_comment`).
- When a comment body equals `/jira` (case-insensitive), the service creates an issue in Jira using the Jira REST API.

The main implementation is in `test.py` (function `createJIRA`).

## Files

- `test.py` — main Flask app and webhook handler.

## Prerequisites

- Python 3.8+
- A Jira Cloud account with an API token (or other Jira REST credentials).

## Environment variables

Set these before running the app. Example names used by `test.py`:

- `JIRA_URL` — base URL for your Jira instance (e.g. `https://yourcompany.atlassian.net`).
- `JIRA_API_TOKEN` — API token for the Jira account.
- `JIRA_EMAIL` — email address for the Jira account.

## Installation

Install required Python packages (recommended to use a virtualenv):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install flask requests
```

You can also create a `requirements.txt` with:

```
flask
requests
```

and install with `pip install -r requirements.txt`.

## Run (development)

In PowerShell, set the environment variables and start the Flask app:

```powershell
#$env:JIRA_URL = "https://yourcompany.atlassian.net"
#$env:JIRA_API_TOKEN = "your_api_token"
#$env:JIRA_EMAIL = "you@example.com"
python test.py
```

The app listens by default on `0.0.0.0:5000` (Flask debug server). For production, run behind a WSGI server (gunicorn/uwsgi) and secure credentials.

## Endpoint

- POST `/createJIRA`
  - Expects a GitHub webhook payload.
  - Requires header `X-GitHub-Event: issue_comment`.
  - Only triggers when the comment body equals `/jira`.

Sample test curl (local):

```powershell
curl -X POST http://localhost:5000/createJIRA `
  -H "Content-Type: application/json" `
  -H "X-GitHub-Event: issue_comment" `
  -d '{"comment": {"body": "/jira", "user": {"login": "octocat"}}, "issue": {"html_url": "https://github.com/org/repo/issues/123"}}'
```

## Implementation notes

- The Jira payload is built in `test.py` and posts to `${JIRA_URL}/rest/api/3/issue`.
- You should update the `project.key` (`"AB"`) and `issuetype.id` values to match your Jira setup.

## Security & production suggestions

- Verify GitHub webhook signatures (HMAC) before trusting payloads.
- Do not run Flask's debug server in production.
- Use environment variable management (secrets manager, .env with proper protections, or CI secrets).

## TODOs

- Validate and verify GitHub webhook signatures.
- Add configurable project key and issue type via env vars or config file.
- Add tests for the webhook handler and Jira request formation.

## Diagrams

Below are two simple Mermaid diagrams illustrating the architecture and the request sequence used by this project. These render on GitHub and many Markdown viewers that support Mermaid. If your viewer doesn't render Mermaid, you can use an online Mermaid live editor (https://mermaid.live) to paste the blocks below and export images.

### Architecture

```mermaid
graph LR
  Dev[Developer / GitHub User] -->|comments on issue| GH[GitHub]
  GH -->|webhook POST /createJIRA| EC2[EC2 Instance (Flask App)]
  EC2 -->|POST /rest/api/3/issue| Jira[Jira Cloud API]
  Jira -->|201 Created| EC2
  EC2 -->|response| GH
```

### Sequence (simplified)

```mermaid
sequenceDiagram
  participant Dev as Developer
  participant GH as GitHub
  participant EC2 as EC2 (Flask)
  participant Jira as Jira Cloud

  Dev->>GH: comment "/jira" on issue
  GH->>EC2: POST /createJIRA (webhook payload)
  EC2->>Jira: POST /rest/api/3/issue (with auth)
  Jira-->>EC2: 201 Created (issue key)
  EC2-->>GH: optional status/response
  EC2-->>Dev: returns webhook handler response
```

## License

Add an appropriate license file if you intend to open-source this project.
=======
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
>>>>>>> 7eca39a15a9b1c1cc1442321699d850a82899703
