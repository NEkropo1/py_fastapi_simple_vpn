from typing import Optional

from pydantic import BaseModel


class Site(BaseModel):
    url: str
    follow_counter: Optional[int] = 0
