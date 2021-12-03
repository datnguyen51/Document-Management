from app import app
from app.controllers.api.permission import (
    router,
    permission
)

app.include_router(router)
