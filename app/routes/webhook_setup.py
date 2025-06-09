from fastapi import APIRouter, HTTPException
from app.clients import trello_client

router = APIRouter()

from pydantic import BaseModel

class WebhookRequest(BaseModel):
    callback_url: str
    model_id: str

@router.post("/setup-webhook")
def setup_trello_webhook(payload: WebhookRequest):
    try:
        result = trello_client.create_webhook(payload.callback_url, payload.model_id)
        return {"status": "success", "webhook_id": result.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
