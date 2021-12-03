from app import app
from app.controllers.api.document_admin import document_admin

app.include_router(document_admin.router)
