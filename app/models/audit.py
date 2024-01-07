from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.config.database import Base

class AuditDB(Base):
    __tablename__ = "audit"

    audit_id = Column(Integer, primary_key=True, index=True)
    audited_at = Column(DateTime)
    status = Column(String)
    audited_by = Column(Integer, ForeignKey("users.id"))
    document_id = Column(Integer, ForeignKey('documents.id'))
    audited = relationship("UserDB", back_populates="audits", single_parent=True)
    document = relationship("DocumentDB", back_populates="audits", single_parent=True)