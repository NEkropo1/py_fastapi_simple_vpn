from sqlalchemy import Column, Integer, String, UniqueConstraint, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship

from middleware.encdec import hash_password, verify_password
from engine import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(LargeBinary, nullable=False)
    personal_data = Column(String, nullable=True)
    sites = relationship("Site", back_populates="user")
    __table_args__ = (
        UniqueConstraint("username", name="unique_username"),
    )

    def set_password(self, password):
        self.password = hash_password(password)

    def check_password(self, password):
        return verify_password(self.password, password)


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="sites")
    follow_counter = Column(Integer, default=0)
    data_uploaded = Column(Integer, default=0)
    data_downloaded = Column(Integer, default=0)
