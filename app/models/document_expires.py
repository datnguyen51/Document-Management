from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID

from app.database.model import CommonModel


class DocumentExpires(CommonModel):
    __tablename__ = "document_expires"
    day = Column(Integer())
    description = Column(String(500))
    unit_id = Column(UUID(as_uuid=True), ForeignKey('unit.id'))
    unit_name = Column(String(250))
    document_type_id = Column(UUID(as_uuid=True), ForeignKey('document_type.id'))
    document_type_name = Column(String(250))
