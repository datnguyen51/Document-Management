from app import app
from app.controllers.api.position import position

app.include_router(position.router)
