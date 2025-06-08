import os
import requests

TRELLO_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_SECRET")
BASE_URL = "https://api.trello.com/1"

def create_webhook(callback_url: str, model_id: str, description: str = "Webhook for PR automation"):
    url = f"{BASE_URL}/webhooks/"
    payload = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN,
        "callbackURL": "https://precious-ultimately-insect.ngrok-free.app/webhooks/trello",
        "idModel": "jizdjjhzhchfzav42jrp",
        "description": "Create card webhook"
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

def comment_on_card(card_id: str, content: str):
    url = f"{BASE_URL}/cards/{card_id}/actions/comments"
    params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN,
        "text": content
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()

def update_card(card_id: str, pr_url: str, test_summary: str, acceptance_criteria: str):
    comment = f"""🔧 Automated Update

🧪 **Acceptance Criteria**
{acceptance_criteria}

✅ **Test Cases**
{test_summary}

🔗 **PR**: {pr_url}
"""
    return comment_on_card(card_id, comment)
