from typing import List
from fastapi import Depends, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from ..models import Post as PostModel
from ..schemas import PostSchema, PostCreateSchema, PostUpdateSchema
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)

# Get all posts
@router.get("/", response_model=List[PostSchema])
def read_posts(db: Session = Depends(get_db)):
    posts = db.query(PostModel).all()

    if not posts:
        raise HTTPException(status_code=404, detail="Posts not found")
    return posts

# Create a new post 
@router.post("/", response_model=PostSchema)
def create_post(post: PostCreateSchema, db: Session = Depends(get_db)):
    new_post = PostModel(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# Read a post
@router.get("/{id}", response_model=PostSchema)
def read_post(id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return post

# Update a post
@router.put("/{id}", response_model=PostSchema)
def update_post(id: int, post: PostUpdateSchema, db: Session = Depends(get_db)):
    post_query = db.query(PostModel).filter(PostModel.id == id)
    to_update = post_query.first()

    if to_update:
        post_query.update(post.model_dump())
        db.commit()
        db.refresh(to_update)
        return to_update
    else:
        raise HTTPException(status_code=404, detail="Post not found")

# Delete a post
@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(post)
    db.commit()
    return Response(status_code=204)
