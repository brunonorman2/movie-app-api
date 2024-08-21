from pydantic import BaseModel, ConfigDict

class MovieBase(BaseModel):
    title: str
    producer: str
    description: str


class Movie(MovieBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
        
class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    pass

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    full_name: str
    password: str

class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)