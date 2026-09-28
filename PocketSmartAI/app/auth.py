from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from passlib.context import CryptContext
from app.config import settings
from app.models.db import User

pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")
def hash_password(x): return pwd.hash(x)
def verify(x,h): return pwd.verify(x,h)
def token(uid):
    exp=datetime.now(timezone.utc)+timedelta(days=1)
    return jwt.encode({"sub":str(uid),"exp":exp},settings().secret_key,algorithm="HS256")
def user_from_token(t):
    try: return int(jwt.decode(t,settings().secret_key,algorithms=["HS256"])["sub"])
    except (JWTError,KeyError,ValueError): return None
