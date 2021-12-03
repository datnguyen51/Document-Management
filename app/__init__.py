import os
from fastapi import FastAPI
from dotenv import load_dotenv
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware

app = FastAPI()

load_dotenv(".env")

URL = os.environ["URL"]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=os.environ["ORIGINS"],
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    DBSessionMiddleware,
    db_url=os.environ["DATABASE_URL"]
)
