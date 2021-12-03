from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.database.model import CommonModel


class DepartmentDocument(CommonModel):
    __tablename__ = "department_document"
    description = Column(String(500))
    document_id = Column(UUID(as_uuid=True), ForeignKey('document.id'))
    document_name = Column(String(250))
    document_type_id = Column(UUID(as_uuid=True))
    department_name = Column(String(250))
    department_id = Column(UUID(as_uuid=True), ForeignKey('department.id'))
