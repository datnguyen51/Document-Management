from app import app
from app.controllers.api.document_manager import document_manager

app.include_router(document_manager.router)
