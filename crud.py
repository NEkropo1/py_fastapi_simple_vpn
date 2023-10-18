from fastapi import HTTPException
from jose import jwt
from sqlalchemy.orm import Session

from auth import SECRET_KEY, ALGORITHM
from middleware.encdec import hash_password
from models import User, Site
from engine import get_session


def create_user(user) -> User:
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        password=hashed_password,
        personal_data=user.personal_data
    )
    with get_session() as session:
        try:
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
        except Exception as e:
            session.rollback()
            raise e
    return db_user


def get_user(username: str) -> User:
    with get_session() as session:
        user = session.query(User).filter(User.username == username).first()
        return user


def get_user_from_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=402, detail="Token expired")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Not found, details: \n{e}")


def get_current_user(username: str, token: str) -> User:
    payload = get_user_from_token(token)
    if payload and payload.get("sub") == username:
        return get_user(username)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


def update_user_data(username, new_data) -> User:
    with get_session() as session:
        db_user = session.query(User).filter(User.username == username).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        db_user.personal_data = new_data
        try:
            session.commit()
            session.refresh(db_user)
        except Exception as e:
            session.rollback()
            raise e
    return db_user


def save_site_to_db(site: Site) -> None:
    with get_session() as session:
        try:
            session.add(site)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e


def create_site(db: Session, site_url: str, current_user: User) -> Site:
    new_site = Site(site_url=site_url, user_id=current_user.id)
    try:
        db.add(new_site)
        db.commit()
        db.refresh(new_site)
    except Exception as e:
        db.rollback()
        raise e
    return new_site
