from fastapi import HTTPException, status
from app.auth.domain.bo.user_bo import userBO
from app.auth.domain.persistence.token_bo import TokenBOPersistenceInterface
from app.auth.domain.persistence.user_bo import UserBOPersistenceInterface




class GetIntrospectController:
    def __init__(self, 
                 token_database: TokenBOPersistenceInterface, 
                 user_database: UserBOPersistenceInterface):
        self.token_database = token_database
        self.user_database = user_database

    async def __call__(self, token: str) -> userBO:
        email = await self.token_database.get(token=token)
        if email is None:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,)
        user = await self.user_database.get(email=email)
        return user