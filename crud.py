from models import User
from engine import SessionLocal as db


def create_user(user):
    db_user = User(username=user.username, password=user.password, personal_data=user.personal_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(username):
    return db.query(User).filter(User.username == username).first()


def update_user_data(username, new_data):
    db_user = db.query(User).filter(User.username == username).first()
    db_user.personal_data = new_data
    db.commit()
    db.refresh(db_user)
    return db_user
