from app import app
from app.controllers.api.staff import staff, staff_list

app.include_router(staff.router)
