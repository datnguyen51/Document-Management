from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.database.model import CommonModel


class Document(CommonModel):
    __tablename__ = "document"
    code = Column(String(250))
    release_code = Column(String(250))
    name = Column(String(2500), nullable=False, index=True)
    description = Column(String(2500))
    file_name = Column(String(2500))
    sign_day = Column(BigInteger())
    received_date = Column(BigInteger())
    signer = Column(String(100))
    status = Column(String(100))
    type = Column(String(250))
    comment = Column(String(2500))
    end_at = Column(BigInteger())
    unit = relationship("Unit", back_populates='document')
    unit_id = Column(UUID(as_uuid=True), ForeignKey('unit.id'))
    unit_name = Column(String(250))
    staff_name = Column(String())
    document_expire = Column(BigInteger())
    document_children = relationship('Document')
    document_parent_id = Column(UUID(as_uuid=True), ForeignKey('document.id'))
    document_parent_name = Column(String())
    document_type = relationship("DocumentType", back_populates='document')
    document_type_id = Column(UUID(as_uuid=True), ForeignKey('document_type.id'))
    document_type_name = Column(String(250))
    work_report = relationship("WorkReport", back_populates='document')
