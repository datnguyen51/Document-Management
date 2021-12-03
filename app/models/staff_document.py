from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.database.model import CommonModel


class StaffDocument(CommonModel):
    __tablename__ = "staff_document"
    status = Column(String(250))
    description = Column(String(500))
    staff_id = Column(UUID(as_uuid=True), ForeignKey('staff.id'))
    staff_name = Column(String(250))
    document_id = Column(UUID(as_uuid=True), ForeignKey('document.id'))
    document_name = Column(String(250))
    document_type_id = Column(UUID(as_uuid=True))
