from datetime import datetime
from sqlalchemy import Column,Integer,String,Text,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    name=Column(String(100),nullable=False)
    email=Column(String(255),unique=True,index=True,nullable=False)
    password_hash=Column(String(255),nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)
    history=relationship("History",back_populates="user",cascade="all,delete-orphan")

class History(Base):
    __tablename__="history"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    planner=Column(String(30),nullable=False)
    request_json=Column(Text,nullable=False)
    response_json=Column(Text,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)
    user=relationship("User",back_populates="history")
