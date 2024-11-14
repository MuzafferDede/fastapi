from datetime import datetime
from pydantic import BaseModel, EmailStr

# Post Schemas
# Shared fields between different Post schemas
class PostBaseSchema(BaseModel):
    title: str
    content: str
    published: bool = True

# Schema for reading a Post (with additional fields like id and created_at)
class PostSchema(PostBaseSchema):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Schema for creating a Post
class PostCreateSchema(PostBaseSchema):
    pass

# Schema for updating a Post
class PostUpdateSchema(PostBaseSchema):
    pass
 
 # ==============================

 # User Schemas
# Shared fields between different User schemas
class UserBaseSchema(BaseModel):
    email: EmailStr

# Schema for reading a User (with additional fields like id and created_at)
class UserSchema(UserBaseSchema):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Schema for creating a User (requires password)
class UserCreateSchema(UserBaseSchema):
    password: str

# Schema for updating a User (optional password update)
class UserUpdateSchema(UserBaseSchema):
    password: str