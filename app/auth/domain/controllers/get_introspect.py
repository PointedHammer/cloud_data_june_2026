from fastapi import HTTPException, status
from app.auth.domain.bo.user_bo import userBO
from app.auth.domain.persistence.token_bo import TokenBOPersistenceInterface
from app.auth.domain.persistence.token_bo import TokenBOPersistenceInterface



class GetIntrospectController:
    def __init__(self, 
                 token_database: TokenBOPersistenceInterface, 
                 user_database: TokenBOPersistenceInterface):
        self.token_database = token_database
        self.user_database = user_database

    def __call__(self, token: str) -> userBO:
        email = self.token_database.get(token=token)
        if email is None:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
        user = self.user_database.get(token=email)

        return user