from fastapi.testclient import TestClient
from app.main import app
c=TestClient(app)
def test_health():
    r=c.get("/api/health")
    assert r.status_code==200 and r.json()["status"]=="ok"
def test_protected():
    assert c.get("/api/session-info").status_code==401
