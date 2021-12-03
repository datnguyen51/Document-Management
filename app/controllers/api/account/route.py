from app.controllers.api.account.login import login
from app import app
from app.controllers.api.account import login
from app.controllers.api.account import account
from app.controllers.api.account import profile
from app.controllers.api.account import account_id
from app.controllers.api.account import create_account
from .account_id import delete_account

app.include_router(account.router)
