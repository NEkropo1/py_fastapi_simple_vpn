from urllib.request import Request

from fastapi import FastAPI, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import middleware.data_uploaded

from auth import create_access_token, verify_token
from engine import get_session
from models import User, Site
from proxies.proxies import get_site_content_with_random_proxy, refactor_site_content, create_endpoint
from schemas.user import UserCreate, UserLogin
from schemas.site import SiteInDB, SiteInResponse, SiteCreate
from utilities.helper_functions import get_user_by_username, get_site_data

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
def login_user(user_data: UserLogin):
    username = user_data.username
    password = user_data.password
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
            user = get_user_by_username(session, username)
            return get_site_data(user)
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.post("/create_site", response_model=SiteInDB)
async def create_site(
        site: SiteCreate,
        current_user: User = Depends(crud.get_current_user),
        db: Session = Depends(get_session)
):
    db_site = crud.create_site(db, site.url, current_user)
    create_endpoint(db_site.url)
    return db_site


@router.get("/site_content/", response_model=SiteInResponse)
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

app.include_router(router)
# TODO: Refactor middleware, it's currently not working
# middleware = middleware.data_uploaded.RequestSizeMiddleware(app, get_session(), Site)
# app.add_middleware(middleware.__class__)
