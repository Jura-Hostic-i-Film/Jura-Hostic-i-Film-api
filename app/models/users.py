from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.models import Base

user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role_id", Integer, ForeignKey("roles.id")),
)


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    roles = relationship("RoleDB", secondary=user_role, back_populates="users", cascade="all, delete")
    documents = relationship("DocumentDB", back_populates="owner")
    audits = relationship("AuditDB", back_populates="audited")
    signatures = relationship("SignatureDB", back_populates="signed")
    #archives = relationship("ArchiveDB", back_populates="archived")

class RoleDB(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    users = relationship("UserDB", secondary=user_role, back_populates="roles", cascade="all, delete")
