
from pydantic import BaseModel, Field, ConfigDict


# Data received during registration
class UserCreate(BaseModel):
    email: str
    password: str = Field(min_length=8)


# Data received during login
class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    email: str | None = None


# Data returned to the client
class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
