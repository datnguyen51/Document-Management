from app import URL
from fastapi import APIRouter


router = APIRouter(
    prefix="/expires" + URL,
    tags=["expires"]
)
