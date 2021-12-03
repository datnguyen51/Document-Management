from app import app
from app.controllers.api.document_expires import document_expires, document

app.include_router(document_expires.router)
