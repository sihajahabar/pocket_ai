from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings
s=settings()
engine=create_engine(s.database_url, connect_args={"check_same_thread":False} if s.database_url.startswith("sqlite") else {})
SessionLocal=sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base=declarative_base()
def db_session():
    db=SessionLocal()
    try: yield db
    finally: db.close()
