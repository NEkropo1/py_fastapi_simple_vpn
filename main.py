from urllib.request import Request

from fastapi import FastAPI, HTTPException

from crud import create_user, get_user, update_user_data
from auth import create_access_token, verify_token
from models import User, Site
from schemas.user import UserCreate

app = FastAPI()


@app.middleware("http")
async def count_requests(request: Request, call_next):
    response = await call_next(request)
    return response


@app.post("/register/")
def register_user(user: UserCreate):
    if len(user.password) < 5 or len(user.password) > 12:
        raise HTTPException(status_code=400, detail="Password length should be between 5 and 12 characters")
    existing_user = get_user(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    created_user = create_user(user)
    return {"message": "User registered successfully", "user": created_user}


@app.post("/login/")
def login_user(username: str, password: str):
    user = get_user(username)
    if user and user.check_password(password):
        token = create_access_token({"sub": user.username})
        return {"message": "Login successful", "token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.put("/edit_data/")
def edit_user_data(username: str, new_data: str, token: str):
    payload = verify_token(token)
    if payload and payload.get("sub") == username:
        updated_user = update_user_data(username, new_data)
        return {"message": "Personal data updated successfully", "user": updated_user}
    raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/statistics/")
def get_statistics(token: str, username: str):
    payload = verify_token(token)
    if payload and payload.get("sub") == username:
        user = get_user(username)
        if user:
            return {"message": f"{user.personal_data}"}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    raise HTTPException(status_code=401, detail="Unauthorized")
