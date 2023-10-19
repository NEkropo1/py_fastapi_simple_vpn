from pydantic import BaseModel, constr
from typing import List, Optional


class UserCreate(BaseModel):
    username: constr(min_length=5, max_length=12)
    password: constr(min_length=5, max_length=12)
    personal_data: Optional[str]
    sites: Optional[List[str]] = []

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def create_with_empty_personal_data(cls, **kwargs):
        if "personal_data" not in kwargs:
            kwargs["personal_data"] = ""
        return cls(**kwargs)


class UserLogin(BaseModel):
    username: str
    password: str
