from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.database.model import CommonModel


class DocumentType(CommonModel):
    __tablename__ = "document_type"
    name = Column(String(50), nullable=False, index=True)
    description = Column(String(250))
    document = relationship("Document", back_populates='document_type')
    unit = relationship('Unit', secondary='document_expires', backref='document_type', cascade="all")
