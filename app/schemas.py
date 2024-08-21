from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class User(UserBase):
    id: int
    email: str

    class Config:
        orm_mode = True
