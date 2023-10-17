from sqlalchemy import Column, Integer, String, UniqueConstraint, CheckConstraint
from engine import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String, nullable=False)
    personal_data = Column(String, nullable=True)
    __table_args__ = (
        UniqueConstraint("username", name="unique_username"),
        CheckConstraint(
            "CHAR_LENGTH(password) >= 5 and CHAR_LENGTH(password) <= 12",
            name="password_length_check"
        ),
    )
