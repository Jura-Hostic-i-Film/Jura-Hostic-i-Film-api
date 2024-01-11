from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, DateTime
from sqlalchemy.orm import relationship

from app.config.database import Base


class DocumentDB(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey('images.id'))
    owner_id = Column(Integer, ForeignKey('users.id'))
    document_type = Column(String)
    summary = Column(String)
    document_status = Column(String)
    scan_time = Column(DateTime)
    image = relationship("ImageDB", back_populates="document", single_parent=True)
    owner = relationship("UserDB", back_populates="documents", single_parent=True)
    audit = relationship("AuditDB", back_populates="document", single_parent=True)
    signatures = relationship("SignatureDB", back_populates="document", single_parent=True)


class ImageDB(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    image_file = Column(LargeBinary, nullable=True)
    document = relationship("DocumentDB", back_populates="image", single_parent=True)
