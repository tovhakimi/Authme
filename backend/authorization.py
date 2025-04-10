from fastapi import Request, HTTPException
from backend.auth import verify_token


def require_role(*roles: str):
    def wrapper(request: Request):
        token = request.headers.get("Authorization")
        
        if not token or not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization token missing or invalid")
    
        token = token.split(" ")[1]
        decoded = verify_token(token)
        
        if decoded["role"] not in roles:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        return decoded
    return wrapper
        