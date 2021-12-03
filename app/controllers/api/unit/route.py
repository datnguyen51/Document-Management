from app import app
from app.controllers.api.unit import unit

app.include_router(unit.router)
