from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.config.database import Base


class ArchiveDB(Base):
    __tablename__ = "archives"

    archive_number = Column(Integer, primary_key=True, index=True)
    status = Column(String)
    archive_at = Column(DateTime)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    archive_by = Column(Integer, ForeignKey("users.id"))
    document = relationship("DocumentDB", back_populates="archives", single_parent=True)
    archived = relationship("UserDB", back_populates="archives", single_parent=True)
