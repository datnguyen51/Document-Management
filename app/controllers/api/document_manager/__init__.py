from app import URL
from fastapi import APIRouter


router = APIRouter(
    prefix="/manager" + URL,
    tags=["manager"]
)
