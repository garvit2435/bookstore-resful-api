from pydantic import BaseModel

class BookBase(BaseModel):  # Define BookBase
    title: str
    author: str
    isbn: str
    price: float
    quantity: int

class BookCreate(BookBase):  # Inherits from BookBase
    pass

class Book(BookBase):  # Inherits from BookBase
    id: int  # Additional field in the Book model

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

