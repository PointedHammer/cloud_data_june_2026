from typing import Optional
from pydantic import BaseModel

class userBO(BaseModel):
    email: str
    hashed_password: str
    address: Optional[str] = None