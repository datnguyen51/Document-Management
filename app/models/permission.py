from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.database.model import CommonModel


class Permission(CommonModel):
    __tablename__ = "permission"
    name = Column(String(150), nullable=False, index=True)
    method = Column(String(2500))
    type = Column(String(250))
