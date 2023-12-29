from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from app.config.database import Base

audit_users = Table(
    "audit_users",
    Base.metadata,
    Column("audit_id", Integer, ForeignKey("audit.audit_id")),
    Column("user_id", Integer, ForeignKey("users.id")),
)

audit_documents = Table(
    "audit_documents",
    Base.metadata,
    Column("audit_id", Integer, ForeignKey("audit.audit_id")),
    Column("document_id", Integer, ForeignKey("documents.id")),
)

class AuditDB(Base):
    __tablename__ = "audit"

    audit_id = Column(Integer, primary_key=True, index=True)
    audited_at = Column(DateTime)
    status = Column(String)
    audited_by = relationship("UserDB", secondary=audit_users, back_populates="audits", cascade="all, delete")
    document_id = relationship("DocumentDB", secondary=audit_documents, back_populates="audits", cascade="all, delete")