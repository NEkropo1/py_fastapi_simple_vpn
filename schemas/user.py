from pydantic import BaseModel, constr
from typing import List, Optional


class UserCreate(BaseModel):
    username: constr(min_length=5, max_length=12)
    password: constr(min_length=5, max_length=12)
    personal_data: str
    sites: Optional[List[str]] = []

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
