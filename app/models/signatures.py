from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.config.database import Base


class SignatureDB(Base):
    __tablename__ = "signatures"

    signature_id = Column(Integer, primary_key=True, index=True)
    status = Column(String)
    signed_at = Column(DateTime, nullable=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    sign_by = Column(Integer, ForeignKey("users.id"))
    document = relationship("DocumentDB", back_populates="signatures", single_parent=True)
    signed = relationship("UserDB", back_populates="signatures", single_parent=True)
