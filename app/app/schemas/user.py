from typing import Optional, List

from pydantic import BaseModel, UUID4


# Shared properties
class UserBase(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    social_urls: List[str] = None
    is_superuser: Optional[bool] = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    name: str
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: UUID4
    name: str
    is_active: bool

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
