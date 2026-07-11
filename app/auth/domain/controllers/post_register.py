from fastapi import HTTPException, status
from typing import Optional
from app.auth.domain.bo.user_bo import userBO as UserBO
from app.auth.domain.persistence.user_bo import UserBOPersistenceInterface
from app.auth.domain.services.computed_hashed_password_service import ComputeHashedPasswordService



class PostRegisterController:
    def __init__(self, 
                 user_database: UserBOPersistenceInterface,
                 ):
        self.user_database = user_database
        self.compute_hashed_pasword_service = ComputeHashedPasswordService()

    async def __call__(self, email: str, password: str, address: Optional[str] = None) -> UserBO:
        if await self.user_database.exists(user_email=email):
                    raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail="User already exists")
        current_new_user = UserBO(            
            email=email,
            hashed_password=self.compute_hashed_pasword_service(email, password),
            address=address
        )
        await self.user_database.create(user=current_new_user)

        return current_new_user