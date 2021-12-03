from app import app
from app.controllers.api.department import department, department_list, department_tree, create_data_department

app.include_router(department.router)
