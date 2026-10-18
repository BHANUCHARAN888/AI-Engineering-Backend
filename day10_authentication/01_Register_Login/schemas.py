from pydantic import BaseModel, Field

class UserRegister(BaseModel):
    username: str
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    username: str
    password: str
