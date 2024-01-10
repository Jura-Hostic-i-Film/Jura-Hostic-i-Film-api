from app.config.database import  engine, SessionLocal
from app.config.database import Base
from app.models.users import RoleDB
from app.utils.enums import RolesEnum


def create_tables():
    Base.metadata.create_all(bind=engine)


def add_roles(db=SessionLocal()):
    for role_name in RolesEnum:
        existing_role = db.query(RoleDB).filter(RoleDB.name == role_name).first()

        if not existing_role:
            new_role = RoleDB(name=role_name)
            db.add(new_role)

    db.commit()
