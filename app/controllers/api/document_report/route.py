from app import app
from app.controllers.api.document_report import (
    router,
    admin,
    manager,
    staff
)

app.include_router(router)
