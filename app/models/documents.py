from sqlalchemy import Column, Integer, String, DATETIME, BLOB, ForeignKey
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
    scan_time = Column(DATETIME)
    image = relationship("ImageDB", back_populates="document", single_parent=True)
    owner = relationship("UserDB", back_populates="documents", single_parent=True)


class ImageDB(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    image_file = Column(BLOB, nullable=True)
    document = relationship("DocumentDB", back_populates="image", single_parent=True)
    # TODO figure out if there is a better alternative for BLOB
