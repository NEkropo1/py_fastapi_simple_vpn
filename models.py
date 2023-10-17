from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    personal_data: str
