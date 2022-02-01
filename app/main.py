import time 
from fastapi import FastAPI, HTTPException, Response, status
import psycopg2
from psycopg2.extras import RealDictCursor
from . import schemas
from typing import Optional
app = FastAPI()

# --------Connecting database--------
while True:
    try:
        conn = psycopg2.connect(host="localhost",database="fastapi",user="postgres",password="<Your postgres instance password>",cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Successful connection established')
        break
    except Exception as err:
        print('Connection to database failed!!')
        print(f'Error: {err}')
        time.sleep(5)

# function to find the post of exact id
def find(id):
    cursor.execute(""" select * from posts where id= %s """,(id,))
    diction = cursor.fetchone()
    return diction

# A list to store all the deleted post 
deleted_posts = []

# function to find in deleted_posts
def find_deleted(id):
    for object in deleted_posts: 
        diction = dict(object)
        if diction['id'] == int(id):
            return diction

# --------Root GET reply--------
@app.get("/")
def root():
    return {"Greetings":"Hello."}

# --------[C]reate post data--------
@app.post("/posts")
def post_data(post: schemas.Post,response: Response):
    cursor.execute(""" insert into posts ("title","content","published","like") values (%s,%s,%s,%s) returning * """,(post.title, post.content, post.published,post.like))
    post = cursor.fetchone()
    conn.commit()
    response.status_code = status.HTTP_201_CREATED
    return {"message": "Post created successfully" , 
            "data": post
            }

# --------[R]ead all the data--------
@app.get("/posts")
def read_all_posts():
    cursor.execute(""" select * from posts """)
    all_posts = cursor.fetchall()
    return {"data":all_posts}

# --------[R]ead a specific data--------
@app.get("/posts/{id}")
def read_specific_post(id:  int):
    post = find(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id: {id} was not found")
    return {"data":post}

# --------[U]pdate the data--------
@app.put("/posts/{id}")
def update_post(id: int,post: schemas.Post):
    find_post = find(id)
    if not find_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id: {id} was not found")
    cursor.execute(""" update posts set title=%s ,content=%s ,published=%s ,"like"=%s ,created_at=%s where id=%s returning * """,(post.title, post.content, post.published,post.like,'now()',id))
    post  = cursor.fetchone()
    conn.commit()
    return {"message":"post updated successfully",
        "data":post}


# --------[Delete] the data--------
@app.delete("/posts/{id}")
def delete_post(id: int , response: Response):
    post = find(id)
    deleted_post = find_deleted(id)
    if deleted_post:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"message":"This post is already deleted"}
    elif not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    else:
        cursor.execute(""" delete from posts where id=%s """,(id,))
        conn.commit()
        deleted_posts.append(post)
        print(deleted_posts)
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"message":"Deleted successfully","data":post}
