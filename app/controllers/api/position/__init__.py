from app import URL
from fastapi import APIRouter


router = APIRouter(
    prefix="/position" + URL,
    tags=["position"]
)
