from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from app.card_requirements_crew.run import run as run_card_requirements_crew
from app.clients.trello_client import get_trello_card_description
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

processed_cards = set()

@router.head("/")
@router.get("/")
async def webhook_ping():
    return JSONResponse(content={"message": "Trello webhook verified"}, status_code=200)

@router.post("/")
async def handle_trello_webhook(request: Request):
    try:
        logger.info("Calling trello webhook")
        body = await request.json()

        if isinstance(body, str):
            import json
            body = json.loads(body)

        action = body.get('action', {})
        action_type = action.get('type')
        logger.info(f"action type: {action_type}")
        if action_type != 'createCard':
            # No workflow triggered for other actions
            return JSONResponse(status_code=200, content={"message": "Workflow not triggered", "result": None})

        data = action.get("data", {})
        card = data.get("card", {})
        title = card.get("name", "Untitled")
        card_id = card.get("id", "no-card-id")

        if card_id in processed_cards:
            # No workflow triggered for other actions
            return JSONResponse(status_code=200, content={"message": "Card already processed", "result": None})

        description = get_trello_card_description(card_id)

        # Trigger the AI workflow
        result = run_card_requirements_crew({ "title": title, "description": description, "card_id": card_id })
        processed_cards.add(card_id)
        return JSONResponse(status_code=200, content={"message": "Workflow triggered"})
    except Exception as e:
        logger.error(f"Error handling webhook: {e}")
        raise HTTPException(status_code=500, detail="Webhook error")
