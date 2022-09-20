import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import schemas, models



router = APIRouter()


@router.get("/posts",  response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    data = db.query(models.Post).all()
    return data


# Inserting a new post into database
# The below query execution makes us vulnerable to SQL Injection as there is not type-checking of title, content, published:
    # cursor.execute(f"""
    #         INSERT INTO posts (title, content, published) VALUES ({post.title, post.content, post.published})
    #     """)

@router.post('/posts', response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""
    #     INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *
    # """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Get post with id
# The argument of execute should be passed as a tuple


@router.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts where id=%s", (str(id),))
    # post = cursor.fetchone()
    # print(post)
    post = db.query(models.Post).filter(models.Post.id == id).one_or_none()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post with id:%s not found' % id)
    return post

# Delete post with a specific id


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""
    #     DELETE FROM posts WHERE id=%s returning *
    # """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    print(post)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update post with specific id
@router.put('/posts/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""
    #     UPDATE posts SET title = %s, content=%s,published = %s WHERE id=%s RETURNING *
    # """, (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} does not exist')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
