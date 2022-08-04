from lib2to3.pytree import Base
from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    publishes: bool = True
    rating: Optional[int] = None


my_posts = [{
            "title": "Title of the post",
            "content": "Content of the post 1",
            "id": 1
            },
            {
            "title": "Title of the post 2",
            "content": "Content of post 2",
            "id": 2
            }]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


# async keyword is needed if you're calling any asynchronus API
# The decorator allows to modify the behaviour of a function or class.

@app.get("/")
def root():
    return {"message": "Server is up and running"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post('/posts')
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    print(id)
    post = find_post(int(id))
    print(post)
    return {"data": post}
