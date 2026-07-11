import uuid
from app.auth.domain.persistence.token_bo import TokenPersistenceInterface
from app.auth.domain.bo.user_bo import userBO


class TokenMemoryPersistenceService(TokenPersistenceInterface):
    
    def __init__(self):
        self.token_database = {}
        

    def get(self, token: str) -> str:
        return self.token_database[token]

    def generate_token(self, email: str) -> str:
        generated_token = str(uuid.uuid4())
        self.token_database[email] = generated_token
        return generated_token

    def remove(self, token: str):
        if token not in self.token_database:
            raise Exception("Token not found")
        del self.token_database[token]