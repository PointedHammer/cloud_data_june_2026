import uuid

from fastapi import HTTPException, status
from typing import Optional
from app.auth.domain.bo.user_bo import userBO as UserBO
from app.auth.domain.persistence.token_bo import TokenBOPersistenceInterface
from app.auth.domain.persistence.user_bo import UserBOPersistenceInterface
from app.auth.domain.services.computed_hashed_password_service import ComputeHashedPasswordService



class PostLoginController:
    def __init__(self, 
                 user_database: UserBOPersistenceInterface,
                 token_database: TokenBOPersistenceInterface
                 ):
        self.user_database = user_database
        self.token_database = token_database
        self.compute_hashed_pasword_service = ComputeHashedPasswordService()

    async def __call__(self, email: str, password: str) -> str:
        if not await self.user_database.exists(user_email=email):
                    raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail="Email not registered")
        hashed_password = self.compute_hashed_pasword_service(email, password)
        current_user = await self.user_database.get(email=email)
        if current_user.hashed_password != hashed_password:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
        generated_token = self.token_database.generate_token(email)
        return generated_token
        