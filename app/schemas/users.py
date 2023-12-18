from pydantic import BaseModel, EmailStr

from app.utils.enums import RolesEnum


class Role(BaseModel):
    name: RolesEnum

    class Config:
        from_attributes = True
        use_enum_values = True

    def __dict__(self):
        return {"name": self.name}


class RoleWithId(Role):
    id: int


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    username: str


class UserCreate(UserBase):
    password: str
    roles: list[RolesEnum]


class UserLogin(BaseModel):
    username: str
    password: str


class User(UserBase):
    id: int
    roles: list[Role]

    class Config:
        from_attributes = True

    def to_dict(self):
        return {"id": self.id, "email": self.email, "first_name": self.first_name, "last_name": self.last_name,
                "username": self.username, "roles": self.roles}


class AccessToken(BaseModel):
    token: str
