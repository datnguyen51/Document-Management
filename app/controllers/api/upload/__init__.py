from app import URL
from fastapi import APIRouter


router = APIRouter(
    prefix="/upload" + URL,
    tags=["upload"]
)
