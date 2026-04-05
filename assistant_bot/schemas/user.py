from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    id: int
    username: str | None = None

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    # Позволяет Pydantic читать данные напрямую из объектов SQLAlchemy
    model_config = ConfigDict(from_attributes=True)