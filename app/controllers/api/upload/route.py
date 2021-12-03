from app import app
from app.controllers.api.upload import upload, get_file

app.include_router(upload.router)
