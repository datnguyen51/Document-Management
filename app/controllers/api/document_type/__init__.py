from app import URL
from fastapi import APIRouter


router = APIRouter(
    prefix="/document-type" + URL,
    tags=["document-type"]
)
