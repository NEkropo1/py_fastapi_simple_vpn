from .models import User
from .engine import SessionLocal


# Create a new user
def create_user(db, user):
    db_user = User(username=user.username, password=user.password, personal_data=user.personal_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Get a user by username
def get_user(db, username):
    return db.query(User).filter(User.username == username).first()


# Update personal data for a user
def update_user_data(db, username, new_data):
    db_user = db.query(User).filter(User.username == username).first()
    db_user.personal_data = new_data
    db.commit()
    db.refresh(db_user)
    return db_user
