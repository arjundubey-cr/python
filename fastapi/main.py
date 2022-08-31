from typing import List, Optional
from fastapi import FastAPI, HTTPException, status, Depends, Response
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db
import utils

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Connecting to the database
# Try to reconnect to the database every 2sec until the success
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi',
#                                 user='postgres', password='Arjun@2001', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successfull')
#         break
#     except Exception as error:
#         print('Connecting to database failed')
#         print(f'Error: {error}')
#         time.sleep(2)


# async keyword is needed if you're calling any asynchronus API
# The decorator allows to modify the behaviour of a function or class.

@app.get("/")
def root():
    return {"message": "Server is up and running"}

# Get all the posts


@app.get("/posts",  response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    data = db.query(models.Post).all()
    return data


# Inserting a new post into database
# The below query execution makes us vulnerable to SQL Injection as there is not type-checking of title, content, published:
    # cursor.execute(f"""
    #         INSERT INTO posts (title, content, published) VALUES ({post.title, post.content, post.published})
    #     """)

@app.post('/posts', response_model=schemas.Post)
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


@app.get("/posts/{id}", response_model=schemas.Post)
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


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
@app.put('/posts/{id}', response_model=schemas.Post)
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


@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash the password of user
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/users/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user
