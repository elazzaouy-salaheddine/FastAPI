from fastapi import Response, status, APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import models
from ..models import Blog
from ..schemas import Post
from ..database import get_db


router = APIRouter(
    tags=['Posts']
)


@router.get("/posts")
async def posts(db: Session = Depends(get_db)):
    posts = db.query(models.Blog).all()
    return {'posts': posts}


@router.get("/posts/{id}")
async def post_detail(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post not found 404 ")
    return {'post id': post}


@router.post('/create/', status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = Blog(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def post_delete(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Blog).filter(models.Blog.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='post not found')
    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}")
async def post_update(id: int, updated_post: Post,
                      db: Session = Depends(get_db)):
    post_qs = db.query(models.Blog).filter(models.Blog.id == id)
    post = post_qs.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post withe id:{id} does not exist 404")
    post_qs.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_qs.first()}
