import uvicorn
from app import app
from app.controllers import init_controllers

init_controllers(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999)
