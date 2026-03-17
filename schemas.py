from pydantic import BaseModel

class BlogCreate(BaseModel):
    title: str
    content: str
    author: str

class BlogUpdate(BaseModel):
    title: str | None = None
    content: str | None = None