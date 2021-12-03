from app import app
from app.controllers.api.user_role import (
    router,
    role
)

app.include_router(router)
