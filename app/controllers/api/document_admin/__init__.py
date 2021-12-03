from app import URL
from typing import Optional
from fastapi import APIRouter
from pydantic.main import BaseModel


router = APIRouter(
    prefix="/admin" + URL,
    tags=["admin"]
)


class SchemaDocument(BaseModel):
    department_id: Optional[list] = None

    class Config:
        orm_mode = True
