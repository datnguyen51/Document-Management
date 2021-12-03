from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.database.model import CommonModel


class Department(CommonModel):
    __tablename__ = "department"
    name = Column(String(150), nullable=False, index=True)
    description = Column(String(2500))
    created_at = Column(BigInteger())
    staff = relationship("Staff", back_populates='department')
    parent_id = Column(UUID(as_uuid=True), ForeignKey('department.id'))
    parent_name = Column(String(250))
    children = relationship('Department')
    document = relationship(
        'Document', secondary='department_document', backref='department', cascade="all")
    work_report = relationship("WorkReport", back_populates='department')
