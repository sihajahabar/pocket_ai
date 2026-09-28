import json
from app.models.db import History
from app.services.ai import generate

def save(db,user_id,planner,data,image=None,mime=None):
    x=generate(planner,data,image,mime)
    h=History(user_id=user_id,planner=planner,request_json=json.dumps(data),response_json=json.dumps(x))
    db.add(h); db.commit(); db.refresh(h); x["history_id"]=h.id
    return x
