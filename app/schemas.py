from pydantic import BaseModel
# --------Pydantic data below--------

# This is to create a scheme for POST data
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    like: bool = None

# This is to create schema for the response data
class Get_Response(BaseModel):
    title: str
    content: str
    published: bool = True
    like: bool = None
    