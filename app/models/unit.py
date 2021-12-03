from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.database.model import CommonModel


class Unit(CommonModel):
    __tablename__ = "unit"
    name = Column(String(150), nullable=False, index=True)
    description = Column(String(2500))
    document = relationship("Document", back_populates='unit')
