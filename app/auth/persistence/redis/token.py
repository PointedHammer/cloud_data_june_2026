import uuid, redis
from app.auth.domain.persistence.token_bo import TokenPersistenceInterface
from app.auth.domain.bo.user_bo import userBO


class TokenRedisPersistenceService(TokenPersistenceInterface):
    
    def __init__(self):
        self.redis_connection = redis.Redis(host='redis-database',
                                            port=6379, 
                                            decode_responses=True,
                                            )
        

    def get(self, token: str) -> str:
        return self.redis_connection.get(token)

    def generate_token(self, email: str) -> str:
        generated_token = str(uuid.uuid4())
        self.redis_connection.set(email, generated_token)
        return generated_token

    def remove(self, token: str):
        if not self.redis_connection.exists(token):
            raise Exception("Token not found")
        self.redis_connection.delete(token)