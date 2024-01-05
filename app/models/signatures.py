from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import registry
from app.config.database import Base
from pydantic import BaseModel

mapper_registry = registry()


class SignatureDB(Base):
    __tablename__ = "signatures"

    signature_id = Column(Integer, primary_key=True, index=True)
    status = Column(String)
    signed_at = Column(DateTime)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    sign_by = Column(Integer, ForeignKey("users.id"))
    documents = relationship("DocumentDB", back_populates="signatures", single_parent=True)
    signed = relationship("UserDB", back_populates="signatures", single_parent=True)
    owner = relationship("UserDB", back_populates="signatures", single_parent=True)

mapper_registry.configure()
