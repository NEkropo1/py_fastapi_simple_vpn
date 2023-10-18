from sqlalchemy import Column, Integer, String, UniqueConstraint, CheckConstraint, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

from middleware.encdec import hash_password, verify_password

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(LargeBinary, nullable=False)
    personal_data = Column(String, nullable=True)
    __table_args__ = (
        UniqueConstraint("username", name="unique_username"),
    )

    def set_password(self, password):
        self.password = hash_password(password)

    def check_password(self, password):
        return verify_password(self.password, password)
