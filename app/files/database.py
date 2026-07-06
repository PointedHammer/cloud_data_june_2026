from ..config import DATABASE_URL

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