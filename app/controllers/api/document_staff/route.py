from app import app
from app.controllers.api.document_staff import router, document_staff

app.include_router(router)
