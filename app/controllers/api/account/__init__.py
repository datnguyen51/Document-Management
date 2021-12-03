from app import URL
from fastapi import APIRouter


router = APIRouter(
    prefix="/account" + URL,
    tags=["account"]
)
