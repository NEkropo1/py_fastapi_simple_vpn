from typing import Optional

from pydantic import BaseModel

from models import User


class SiteCreate(BaseModel):
    url: str
    follow_counter: Optional[int] = 0

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class SiteInDB(BaseModel):
    site_url: str
    user_id: int
    follow_counter: Optional[int]
    data_uploaded: Optional[int]
    data_downloaded: Optional[int]
    user: User

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class SiteInResponse(BaseModel):
    id: int
    url: str
    user_id: int
    follow_counter: int
    data_uploaded: int
    data_downloaded: int

    class Config:
        from_attributes = True
