from app import app
from app.controllers.api.statistic import (
    router,
    admin,
    manager,
    staff,
    document
)

app.include_router(router)
