from app import URL
from fastapi import APIRouter


router = APIRouter(
    prefix="/permission" + URL,
    tags=["permission"]
)
