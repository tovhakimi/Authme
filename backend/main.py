from fastapi import FastAPI, Depends
from backend.auth import login, register, get_current_user
from backend.authorization import require_role
from backend.db.database import engine
from backend.db.models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/login")
def login_user(username: str, password: str):
    result = login(username, password)
    return result

@app.post("/register")
def register_user(username: str, password: str, role: str):
    return register(username, password, role)

@app.get("/protected")
def protected_route(user=Depends(get_current_user)):
    return{
        "message": "Token is valid",
        "user": user
    }
    
@app.get("/me")
def get_me(user=Depends(get_current_user)):
    return{
        "message": "User info",
        "user": user
    }
    
@app.get("/admin")
def admin_only(user=Depends(require_role("Admin"))):
    return {"message": f"Hello {user['username']}, you are an admin"}