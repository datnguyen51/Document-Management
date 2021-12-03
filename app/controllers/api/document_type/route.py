from app import app
from app.controllers.api.document_type import document_type

app.include_router(document_type.router)
