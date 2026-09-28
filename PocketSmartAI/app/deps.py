from fastapi import Depends,HTTPException,Request
from sqlalchemy.orm import Session
from app.database import db_session
from app.models.db import User
from app.auth import user_from_token

def current_user(request:Request,db:Session=Depends(db_session)):
    t=request.cookies.get("access_token") or request.headers.get("Authorization","").replace("Bearer ","",1)
    uid=user_from_token(t) if t else None
    u=db.get(User,uid) if uid else None
    if not u: raise HTTPException(401,"Authentication required")
    return u
