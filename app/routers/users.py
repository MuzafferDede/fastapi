from typing import List
from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from ..utils import hash
from ..models import User as UserModel
from ..schemas import UserSchema, UserCreateSchema, UserUpdateSchema
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# Get all users
@router.get("/", response_model=List[UserSchema])
def read_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()

    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users

# Create a new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    user.password = hash(user.password)

    new_user = UserModel(**user.model_dump())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Read a user
@router.get("/{id}", response_model=UserSchema)
def read_user(id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

# Update a user
@router.put("/{id}", response_model=UserSchema)
def update_user(id: int, user: UserUpdateSchema, db: Session = Depends(get_db)):
    user_query = db.query(UserModel).filter(UserModel.id == id)
    to_update = user_query.first()

    if to_update:
        user.password = hash(user.password)
        user_query.update(user.model_dump())
        db.commit()
        db.refresh(to_update)
        return to_update
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
# Delete a user
@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return Response(status_code=204)
