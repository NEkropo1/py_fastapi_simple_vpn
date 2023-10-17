from pydantic import BaseModel, constr


class UserCreate(BaseModel):
    username: constr(min_length=5, max_length=12)
    password: constr(min_length=5, max_length=12)
    personal_data: str