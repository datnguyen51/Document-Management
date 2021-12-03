from app import URL
from fastapi import APIRouter


router = APIRouter(
    prefix="/unit" + URL,
    tags=["unit"]
)
