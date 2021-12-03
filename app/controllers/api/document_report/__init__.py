from app import URL
from fastapi import APIRouter


router = APIRouter(
    prefix="/document-report" + URL,
    tags=["document-report"]
)
