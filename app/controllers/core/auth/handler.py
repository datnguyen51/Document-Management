import os
import jwt
import time

from typing import Dict
from dotenv import load_dotenv
from gatco_restapi.helpers import to_dict

from app.controllers.core.utils.data.convert import convert_day_to_timestamp

load_dotenv(".env")

JWT_SECRET = os.environ["SECRET_KEY"]
JWT_ALGORITHM = os.environ["ALGORITHM"]


def token_response(token: str):
    return token


def signJWT(user) -> Dict[str, str]:
    payload = to_dict(user)
    payload["exp"] = convert_day_to_timestamp(30)
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}
