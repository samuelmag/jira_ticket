from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
import json
import os

app = Flask(__name__)

# --- Environment Variables ---
JIRA_URL = os.environ.get("JIRA_URL")
API_TOKEN = os.environ.get("JIRA_API_TOKEN")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL")

@app.route("/createJIRA", methods=['POST'])
def createJIRA():
    # --- Get JSON payload ---
    data = request.get_json()
    if not data:
        return jsonify({"error": "Empty payload"}), 400

    # --- Check GitHub event type ---
    event_type = request.headers.get("X-GitHub-Event")
    if event_type != "issue_comment":
        return jsonify({"message": f"Ignored event type: {event_type}"}), 200

    # --- Safely extract comment info ---
    comment_body = data.get('comment', {}).get('body', '')
    issue_url = data.get('issue', {}).get('html_url', '')
    user = data.get('comment', {}).get('user', {}).get('login', '')

    # --- Trigger only on '/jira' comment ---
    if comment_body.strip().lower() != "/jira":
        return jsonify({"message": "Not a Jira creation request"}), 200

    # --- Prepare Jira Issue Payload ---
    payload = json.dumps({
        "fields": {
            "summary": f"GitHub Issue: {issue_url.split('/')[-1]}",
            "project": {"key": "AB"},  # Adjust as needed
            "issuetype": {"id": "10080"},  # Adjust as needed
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Issue created from GitHub:\nURL: {issue_url}\nComment by {user}: {comment_body}"
                            }
                        ]
                    }
                ]
            }
        }
    })

    # --- Send request to Jira ---
    auth = HTTPBasicAuth(JIRA_EMAIL, API_TOKEN)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    response = requests.post(
        f"{JIRA_URL}/rest/api/3/issue",
        headers=headers,
        data=payload,
        auth=auth
    )

    # --- Handle Jira response ---
    if response.status_code == 201:
        return jsonify({"message": "Jira issue created!", "key": response.json()["key"]}), 201
    else:
        return jsonify({
            "error": "Failed to create Jira issue",
            "status_code": response.status_code,
            "response": response.text
        }), response.status_code

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
