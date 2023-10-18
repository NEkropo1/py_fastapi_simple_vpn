from urllib.request import Request

from fastapi import FastAPI, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import models

from auth import create_access_token, verify_token
from engine import get_session
from models import User, Site
from proxies.proxies import get_site_content_with_random_proxy, refactor_site_content
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
async def get_statistics(token: str, username: str) -> dict:
    payload = verify_token(token)
    if payload and payload.get("sub") == username:
        with get_session() as session:
            user = session.query(models.User).filter(models.User.username == username).first()
            if user:
                sites_data = {
                    site.url: {
                        "follow_counter": site.follow_counter,
                        "data_uploaded": site.data_uploaded,
                        "data_downloaded": site.data_downloaded
                    } for site in user.sites
                }
                return sites_data if sites_data else {"message": "No sites created yet."}
            else:
                raise HTTPException(status_code=404, detail="User not found")
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.post("/create_site", response_model=Site)
async def create_site(site: Site, current_user: User = Depends(crud.get_current_user), db: Session = Depends(get_session)):
    db_site = crud.create_site(db, site, current_user)
    route_link = f"{site.url}/"
    return {"route_link": route_link, "site": db_site}


@router.get("/site_content/")
async def get_site_content(
        token: str,
        user_site_name: str,
        routes_on_original_site: str
):
    payload = verify_token(token)
    if payload:
        original_site_url = f"{user_site_name}/{routes_on_original_site}"
        site_content = await get_site_content_with_random_proxy(original_site_url)
        refactored_content = refactor_site_content(site_content, user_site_name)
        return refactored_content
    raise HTTPException(status_code=401, detail="Unauthorized")
