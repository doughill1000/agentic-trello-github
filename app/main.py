from fastapi import FastAPI
from app.routers import trello_webhook, webhook_setup

app = FastAPI(title="Trello PR Orchestrator")

# Register routers
app.include_router(trello_webhook.router, prefix="/webhooks/trello", tags=["Trello Webhook"])
app.include_router(webhook_setup.router, prefix="/setup", tags=["Trello Setup"])

@app.get("/")
def health_check():
    return {"status": "ok"}