from tortoise import fields
from tortoise.models import Model

class User(Model):
    email: str
    hashed_password: str
    address: str