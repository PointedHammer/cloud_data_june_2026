from toroise import fields
from tortoise.models import Model

class User(Model):
    email = fields.CharField(pk=True, max_length=255)
    hashed_password = fields.CharField(max_length=64)
    address = fields.CharField(max_length=255, null=True, default=None)

    class Meta:
        table = "users"
        