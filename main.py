from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    number: int
    published: bool = False
    rating: Optional[int]


my_posts = [{"title": "title of post 1",
             "content": "content of post1", "number": "number of user", "id": 1}, {"title": "Favorite Actore", "content": "I am a die hard fan of RamCharan", "number": 1234567890, "id": 2}]


def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def posts():
    return {"message": my_posts}


@app.get("/fastapi")
async def fast():
    return {"message": "https://youtu.be/0sOvCWFmrtA Click on this link to learn about FastAPI"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}
# title str, content str, number int


@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    post = find_posts(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"Post with id: {id} was not found"}
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    delete = find_index(id)
    if delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} doesnot exist")
    my_posts.pop(delete)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    update = find_index(id)
    if update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} doesnot exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[update] = post_dict
    return {'data': post_dict}
