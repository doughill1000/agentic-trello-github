from fastapi import FastAPI
from app.routes import trello_webhook, webhook_setup
import logging

logging.basicConfig(
    level=logging.INFO,  # or DEBUG if you want more detail
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = FastAPI(title="Trello PR Orchestrator")

# Register routers
app.include_router(trello_webhook.router, prefix="/webhooks/trello", tags=["Trello Webhook"])
app.include_router(webhook_setup.router, prefix="/setup", tags=["Trello Setup"])

@app.get("/")
def health_check():
    return {"status": "ok"}