from fastapi import APIRouter, HTTPException
from app.clients import trello_client

router = APIRouter()

@router.post("/setup-webhook")
def setup_trello_webhook(callback_url: str, model_id: str):
    try:
        result = trello_client.create_webhook(callback_url, model_id)
        return {"status": "success", "webhook_id": result.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
