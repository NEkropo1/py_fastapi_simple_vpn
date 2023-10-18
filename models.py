from sqlalchemy import Column, Integer, String, UniqueConstraint, LargeBinary, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from middleware.encdec import hash_password, verify_password

Base = declarative_base()


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
    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="sites")
    site_derivatives = relationship("SiteDerivative", back_populates="site")


class SiteDerivative(Base):
    __tablename__ = "site_derivatives"

    id = Column(Integer, primary_key=True, index=True)
    link = Column(String, unique=True)
    count = Column(Integer)
    site_id = Column(Integer, ForeignKey("sites.id"))
    site = relationship("Site", back_populates="site_derivatives")
