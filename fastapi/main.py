from multiprocessing import synchronize
import time
from typing import Optional
from fastapi import FastAPI, HTTPException, status, Depends, Response
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# Connecting to the database
# Try to reconnect to the database every 2sec until the success
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='Arjun@2001', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successfull')
        break
    except Exception as error:
        print('Connecting to database failed')
        print(f'Error: {error}')
        time.sleep(2)


@app.post('/sqlalchemy')
def test_connection(db: Session = Depends(get_db)):
    data = db.query(models.Post).add_column
    return {
        "data": data
    }


# async keyword is needed if you're calling any asynchronus API
# The decorator allows to modify the behaviour of a function or class.

@app.get("/")
def root():
    return {"message": "Server is up and running"}

# Get all the posts


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    data = db.query(models.Post).all()
    return {
        "data": data
    }


# Inserting a new post into database
# The below query execution makes us vulnerable to SQL Injection as there is not type-checking of title, content, published:
    # cursor.execute(f"""
    #         INSERT INTO posts (title, content, published) VALUES ({post.title, post.content, post.published})
    #     """)

@app.post('/posts')
def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""
    #     INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *
    # """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


# Get post with id
# The argument of execute should be passed as a tuple


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts where id=%s", (str(id),))
    # post = cursor.fetchone()
    # print(post)
    post = db.query(models.Post).filter(models.Post.id==id).one_or_none()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post with id:%s not found' % id)
    return {"data": post}

# Delete post with a specific id


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""
    #     DELETE FROM posts WHERE id=%s returning *
    # """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    delete_post = db.query(models.Post).filter(models.Post.id == id)

    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update post with specific id
@app.put('/posts/{id}')
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    cursor.execute("""
        UPDATE posts SET title = %s, content=%s,published = %s WHERE id=%s RETURNING *
    """, (post.title, post.content, post.published, str(id),))

    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} does not exist')

    return {"data": updated_post}
