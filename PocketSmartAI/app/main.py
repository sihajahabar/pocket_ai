import json
from contextlib import asynccontextmanager
from fastapi import FastAPI,Depends,HTTPException,Request,File,UploadFile,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import Base,engine,db_session
from app.models.db import User,History
from app.models.schemas import Register,Login,Home,Party
from app.auth import hash_password,verify,token
from app.deps import current_user
from app.services.history import save
from app.config import settings

@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(bind=engine)
    yield

app=FastAPI(title="PocketSmart AI",version="1.0.0",lifespan=lifespan)
s=settings()
app.add_middleware(CORSMiddleware,allow_origins=s.origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.mount("/static",StaticFiles(directory="app/static"),name="static")
templates=Jinja2Templates(directory="app/templates")

@app.get("/",response_class=HTMLResponse)
def index(request:Request): return templates.TemplateResponse("index.html",{"request":request})
@app.get("/login",response_class=HTMLResponse)
def login_page(request:Request): return templates.TemplateResponse("login.html",{"request":request})
@app.get("/register",response_class=HTMLResponse)
def register_page(request:Request): return templates.TemplateResponse("register.html",{"request":request})
@app.get("/dashboard",response_class=HTMLResponse)
def dashboard(request:Request,u=Depends(current_user)): return templates.TemplateResponse("dashboard.html",{"request":request,"user":u})
@app.get("/planner/{name}",response_class=HTMLResponse)
def planner(request:Request,name:str,u=Depends(current_user)):
    if name not in ("home","party","jewelry"): raise HTTPException(404,"Planner not found")
    return templates.TemplateResponse(f"{name}.html",{"request":request,"user":u})

@app.post("/auth/register")
def register(data:Register,db:Session=Depends(db_session)):
    email=str(data.email).lower()
    if db.query(User).filter_by(email=email).first(): raise HTTPException(400,"Email already registered")
    u=User(name=data.name.strip(),email=email,password_hash=hash_password(data.password)); db.add(u); db.commit(); db.refresh(u)
    r=RedirectResponse("/dashboard",303); r.set_cookie("access_token",token(u.id),httponly=True,samesite="lax",max_age=86400); return r
@app.post("/auth/login")
def login(data:Login,db:Session=Depends(db_session)):
    u=db.query(User).filter_by(email=str(data.email).lower()).first()
    if not u or not verify(data.password,u.password_hash): raise HTTPException(401,"Invalid credentials")
    r=RedirectResponse("/dashboard",303); r.set_cookie("access_token",token(u.id),httponly=True,samesite="lax",max_age=86400); return r
@app.post("/auth/logout")
def logout():
    r=RedirectResponse("/",303); r.delete_cookie("access_token"); return r
@app.post("/token")
def api_token(data:Login,db:Session=Depends(db_session)):
    u=db.query(User).filter_by(email=str(data.email).lower()).first()
    if not u or not verify(data.password,u.password_hash): raise HTTPException(401,"Invalid credentials")
    return {"access_token":token(u.id),"token_type":"bearer"}

@app.get("/api/health")
def health(): return {"status":"ok","service":"PocketSmart AI"}
@app.get("/api/session-info")
def session_info(u=Depends(current_user)): return {"authenticated":True,"user_id":u.id,"name":u.name,"email":u.email}
@app.get("/api/session-data")
def session_data(u=Depends(current_user),db:Session=Depends(db_session)):
    return {"user_id":u.id,"recommendation_count":db.query(History).filter_by(user_id=u.id).count()}
@app.get("/api/history")
def history(u=Depends(current_user),db:Session=Depends(db_session)):
    rows=db.query(History).filter_by(user_id=u.id).order_by(History.created_at.desc()).all()
    return [{"id":x.id,"planner":x.planner,"created_at":x.created_at.isoformat(),"response":json.loads(x.response_json)} for x in rows]
@app.get("/api/recommendations-details/{hid}")
def details(hid:int,u=Depends(current_user),db:Session=Depends(db_session)):
    x=db.query(History).filter_by(id=hid,user_id=u.id).first()
    if not x: raise HTTPException(404,"Not found")
    return {"id":x.id,"planner":x.planner,"request":json.loads(x.request_json),"response":json.loads(x.response_json)}

@app.post("/api/generate-home")
def generate_home(data:Home,u=Depends(current_user),db:Session=Depends(db_session)): return save(db,u.id,"home",data.model_dump())
@app.post("/api/generate-party")
def generate_party(data:Party,u=Depends(current_user),db:Session=Depends(db_session)): return save(db,u.id,"party",data.model_dump())
@app.post("/api/generate-jewelry")
async def generate_jewelry(budget:float=Form(...),occasion:str=Form(...),style:str=Form("Elegant"),
    outfit_color:str=Form(""),preferences:str=Form(""),outfit:UploadFile|None=File(None),
    u=Depends(current_user),db:Session=Depends(db_session)):
    if budget<=0: raise HTTPException(400,"Budget must be positive")
    image=None; mime=None
    if outfit and outfit.filename:
        if outfit.content_type not in ("image/jpeg","image/png","image/webp"): raise HTTPException(400,"Use JPG, PNG or WEBP")
        image=await outfit.read()
        if len(image)>s.max_upload_mb*1024*1024: raise HTTPException(413,"Image too large")
        mime=outfit.content_type
    data={"budget":budget,"occasion":occasion,"style":style,"outfit_color":outfit_color,"preferences":preferences}
    return save(db,u.id,"jewelry",data,image,mime)
