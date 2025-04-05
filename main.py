from typing import Union

from fastapi import FastAPI
from auth import login

app = FastAPI()

@app.get("/login")
def login_user(username: str, password: str):
    result = login(username, password)
    return result