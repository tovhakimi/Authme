import os
import json
import bcrypt
import jwt
from fastapi import HTTPException, Request
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta
from backend.db.database import SessionLocal
from backend.db.crud import create_user, get_user_by_username, authenticate_user

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_FILE = os.path.join(BASE_DIR, "users.json")

with open('.ssh/id_rsa', 'rb') as f:
    private_key = serialization.load_ssh_private_key(
        f.read(),
        password=None,
        backend=default_backend()
    )
    
with open('.ssh/id_rsa.pub', 'rb') as f:
    public_key = serialization.load_ssh_public_key(
        f.read(),
        backend=default_backend()
    )

def read_users():
    try:
        with open(USERS_FILE, 'r') as users:
            return json.load(users)
    except FileExistsError:
        return {}

def write_users(users):
        with open(USERS_FILE, 'w') as file:
            json.dump(users, file, indent=4)
                
def login(username: str, password: str):
    db = SessionLocal()
    user = authenticate_user(db, username, password)
    
    if not user:
        return {"error": "Invalid username or password"}    
    
    payload_data = {
        "username": user.username,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    
    token = jwt.encode(
        payload=payload_data,
        key=private_key,
        algorithm='RS256'
    )
    return {"message": "Login Successfuly","token": token}

def register(username: str, password: str, role: str):
    db = SessionLocal()
    existing_user = get_user_by_username(db, username)
    
    if existing_user:
        return {"error": "Username already in use"}
    user = create_user(db, username, password, role)
    return {"message": f"User {user.username} registered successfully"}
    
def verify_token(token: str):
    try:
        decode = jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=['RS256']
        )
        return decode
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization token missing or invalid")
    
    token = token.split(" ")[1]
    return verify_token(token)