import os
import json
import bcrypt
import jwt
from fastapi import HTTPException
from cryptography.hazmat.primitives import serialization

private_key = open('.ssh/id_rsa', 'r').read()
public_key = open('.ssh/id_rsa.pub', 'r').read()
key = serialization.load_ssh_private_key(private_key.encode(), password=b'')

def read_users():
    try:
        with open('users.json', 'r') as users:
            return json.load(users)
    except FileExistsError:
        return {}

def write_users(users):
        with open('users.json', 'w') as file:
            json.dump(users, file, indent=4)
                
def login(username: str, password: str):
    users = read_users()
    user = users.get(username)
    
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return {"error": "Invalid Username or Password"}
    
    payload_data = {
        "username": username,
        "role": user.get("role", "User")
    }
    
    token = jwt.encode(
        payload=payload_data,
        key=key,
        algorithm='RS256'
    )
    return {"message": "Login Successfuly","token": token}

def register(username: str, password: str, role: str):
    users = read_users()
    
    if username in users.keys():
        return {"error": "Username is already in use"}
    
    
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