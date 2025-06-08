from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/")
async def handle_trello_webhook(request: Request):
    try:
        body = await request.json()
        logger.info(f"Received Trello webhook: {body}")
        
        card = body.get("action", {}).get("data", {}).get("card", {})
        title = card.get("name", "Untitled")
        description = card.get("desc", "")
        card_id = card.get("id", "no-card-id")

         # Trigger the AI workflow
        result = run_workflow_from_card(title, description, card_id)

        return JSONResponse(status_code=200, content={"message": "Workflow triggered", "result": str(result)})
    except Exception as e:
        logger.error(f"Error handling webhook: {e}")
        raise HTTPException(status_code=500, detail="Webhook error")
