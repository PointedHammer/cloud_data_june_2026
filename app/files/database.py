from app.files.config import DATABASE_URL
from app.files.database import models

models = ["aerich.models", "app.auth.models"]

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},

    "apps": {

        "models": {

            "models": models,

            "default_connection": "default",

        },

    },
}