from app import app
from app.controllers.api.document import (
    router,
    document,
    document_incoming,
    document_internal,
    move_document,
    reject_document
)

app.include_router(router)
