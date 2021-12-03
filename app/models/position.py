from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.database.model import CommonModel


class Position(CommonModel):
    __tablename__ = "position"
    name = Column(String(150), nullable=False, index=True)
    description = Column(String(2500))
    staff = relationship("Staff", back_populates='position')
    parent_id = Column(UUID(as_uuid=True), ForeignKey('position.id'))
    parent_name = Column(String(250))
    children = relationship('Position')
