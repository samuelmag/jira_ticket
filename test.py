from flask import Flask, request  # Added 'request' import
import requests
from requests.auth import HTTPBasicAuth
import json
import os #Import os for environment variables

# Creating a flask app instance
app = Flask(__name__)

@app.route("/createJIRA", methods=['POST'])  # decorator
def createJIRA():
    JIRA_URL = os.environ.get("JIRA_URL")
    API_TOKEN = os.environ.get("JIRA_API_TOKEN") 
    JIRA_EMAIL = os.environ.get("JIRA_EMAIL")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # JIRA payload
    payload = {
        "fields": {
            "description": {
                "content": [
                    {
                        "content": [
                            {
                                "text": "My first jira ticket",
                                "type": "text"
                            }
                        ],
                        "type": "paragraph"
                    }
                ],
                "type": "doc",
                "version": 1
            },
            "issuetype": {
                "id": "10080"
            },
            "project": {
                "key": "AB"
            },
            "summary": "First JIRA Ticket"
        },
        "update": {}
    }

    # Get the webhook JSON data from the request
    webhook = request.json

    # Create a Jira issue if the comment contains '/jira'
    if webhook and 'comment' in webhook and webhook['comment'].get('body') == "/jira":
        response = requests.post(url, json=payload, headers=headers, auth=auth)
        if response.status_code == 201:
            return json.dumps(response.json(), sort_keys=True, indent=4, separators=(",", ": "))
        else:
            return json.dumps({"error": "Failed to create JIRA issue", "details": response.json()}, sort_keys=True, indent=4, separators=(",", ": "))
    else:
        return json.dumps({"message": "Jira issue will be created if comment includes /jira"}, sort_keys=True, indent=4, separators=(",", ": "))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
