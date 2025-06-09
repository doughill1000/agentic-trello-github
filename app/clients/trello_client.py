import os
import requests
from dotenv import load_dotenv
import logging

load_dotenv()

# Initialize logger
logger = logging.getLogger(__name__)

TRELLO_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
BASE_URL = "https://api.trello.com/1"

def create_webhook(callback_url: str, model_id: str, description: str = "Webhook for PR automation"):
    url = f"{BASE_URL}/webhooks/"
    payload = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN,
        "callbackURL": callback_url,
        "idModel": model_id,
        "description": "Create card webhook"
    }

    logger.info(f"Creating Trello webhook with payload: {payload}")

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Trello webhook creation failed: {e}")
        logger.error(f"Response status: {response.status_code}")
        logger.error(f"Response body: {response.text}")
        raise

def get_trello_card_description(card_id):
    """
    Fetches the name and description of a Trello card using the Trello API.

    Args:
        card_id (str): The Trello card ID.

    Returns:
        description
    """
    url = f"https://api.trello.com/1/cards/{card_id}?fields=name,desc&key={TRELLO_KEY}&token={TRELLO_TOKEN}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        card_details = response.json()
        desc = card_details.get("desc", "")
        return desc
    except Exception as e:
        print(f"Error fetching card from Trello: {e}")
        return None

def add_checklist_to_card(card_id: str, title: str, items: list):
    """
    Creates a checklist on the trello card. Then it adds the appropriate items to the checklist

    Args: 
        card_id (str): The Trello card ID.
        title (str): checklist name
        items (list): list of items to be added to the checklist
    """
    # Step 1: Create the checklist
    checklist_url = f"{BASE_URL}/cards/{card_id}/checklists"
    checklist_params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN,
        "name": title
    }
    response = requests.post(checklist_url, params=checklist_params)
    response.raise_for_status()
    checklist_id = response.json()["id"]
    logger.info(f"Added checklist: {title}")

    # Step 2: Add items
    for item in items:
        try:
            item_url = f"{BASE_URL}/checklists/{checklist_id}/checkItems"
            item_params = {
                "key": TRELLO_KEY,
                "token": TRELLO_TOKEN,
            }
            item_data = {
                "name": item,
                "checked": False
            }
            item_response = requests.post(item_url, params=item_params, json=item_data)
            item_response.raise_for_status()
            logger.info(f"Added item: {item}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to add item '{item}' to checklist: {e}")

    return checklist_id


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

def update_card(card_id: str, test_summary: str, acceptance_criteria: str):
    comment = f"""🔧 Automated Update

🧪 **Acceptance Criteria**
{acceptance_criteria}

✅ **Test Cases**
{test_summary}

"""
    return comment_on_card(card_id, comment)

def update_card_description(card_id: str, new_description: str):
    """
    Updates the description of a Trello card.

    Args:
        card_id (str): The ID of the Trello card.
        new_description (str): The new description to set on the card.
    """
    url = f"{BASE_URL}/cards/{card_id}/desc"
    params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN,
        "value": new_description
    }

    try:
        response = requests.put(url, params=params)
        response.raise_for_status()
        logging.info(f"Successfully updated card description for {card_id}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to update card description: {e}")
        return None
