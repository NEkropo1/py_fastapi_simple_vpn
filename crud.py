from fastapi import HTTPException

from middleware.encdec import hash_password
from models import User
from engine import get_session


def create_user(user):
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


def get_user(username):
    with get_session() as session:
        user = session.query(User).filter(User.username == username).first()
        return user


def update_user_data(username, new_data):
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
