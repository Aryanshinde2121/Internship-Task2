from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from database import Base

class Blog(Base):
    __tablename__ = "blogs2"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    content = Column(Text)
    author = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now())