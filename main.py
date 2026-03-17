from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency (DB session)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ POST /blogs → Create blog
@app.post("/blogs", status_code=201)
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    new_blog = models.Blog(**blog.dict())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# ✅ GET /blogs → Get all blogs
@app.get("/blogs")
def get_blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()


# ✅ GET /blogs/{id} → Get blog by ID
@app.get("/blogs/{id}")
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


# ✅ PUT /blogs/{id} → Update blog
@app.put("/blogs/{id}")
def update_blog(id: int, updated: schemas.BlogUpdate, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    if updated.title:
        blog.title = updated.title
    if updated.content:
        blog.content = updated.content

    db.commit()
    return blog


# ✅ DELETE /blogs/{id}
@app.delete("/blogs/{id}")
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    db.delete(blog)
    db.commit()

    return {"message": "Blog deleted successfully"}