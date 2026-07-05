import uuid

from app.auth.domain.bo.user_bo import userBO


class TokenMemoryPersistenceService:
    
    def __init__(self):
        self.token_database = {}

    def get(self, token: str) -> str:
        return self.token_database[token]

    def generate_token(self, email: str) -> str:
        generated_token = str(uuid.uuid4())
        self.token_database[email] = generated_token
        return generated_token

    def create(self, user: userBO) -> userBO:
        self.user_database[user.email] = user
        return user