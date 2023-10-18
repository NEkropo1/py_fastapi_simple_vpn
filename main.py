import json
from urllib.request import Request

from fastapi import FastAPI, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import models

from auth import create_access_token, verify_token
from engine import get_session
from models import User, Site
from schemas.user import UserCreate

app = FastAPI()
router = APIRouter()


@app.middleware("http")
async def count_requests(request: Request, call_next):
    response = await call_next(request)
    return response


@app.post("/register/")
def register_user(user: UserCreate):
    if len(user.password) < 5 or len(user.password) > 12:
        raise HTTPException(status_code=400, detail="Password length should be between 5 and 12 characters")
    existing_user = crud.get_user(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    created_user = crud.create_user(user)
    return {"message": "User registered successfully", "user": created_user}


@app.post("/login/")
def login_user(username: str, password: str):
    user = crud.get_user(username)
    if user and user.check_password(password):
        token = create_access_token({"sub": user.username})
        return {"message": "Login successful", "token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.put("/edit_data/")
def edit_user_data(username: str, new_data: str, token: str):
    payload = verify_token(token)
    if payload and payload.get("sub") == username:
        updated_user = crud.update_user_data(username, new_data)
        return {"message": "Personal data updated successfully", "user": updated_user}
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/statistics/")
async def get_statistics(token: str, username: str) -> json:
    payload = verify_token(token)
    if payload and payload.get("sub") == username:
        with get_session() as session:
            user = session.query(models.User).filter(models.User.username == username).first()
            if user:
                sites_follow_count = {site.url: site.follow_counter for site in user.sites}
                return sites_follow_count if sites_follow_count else {"message": "No sites created yet."}
            else:
                raise HTTPException(status_code=404, detail="User not found")
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.post("/create_site")
async def create_site(site: Site, current_user: User = Depends(crud.get_current_user), db: Session = Depends(get_session)):
    db_site = crud.create_site(db, site, current_user)
    return db_site
