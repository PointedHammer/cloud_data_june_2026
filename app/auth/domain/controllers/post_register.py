from fastapi import HTTPException, status
from typing import Optional
from app.auth.domain.bo.user_bo import userBO as UserBO
from app.auth.domain.persistence.user_bo import UserBOPersistenceInterface
from app.auth.domain.services.compute_hash_password import compute_hash_password



class PostRegisterController:
    def __init__(self, 
                 user_database: UserBOPersistenceInterface,
                 ):
        self.user_database = user_database
        self.compute_hashed_pasword_service = ComputeHashedPaswordService()

    def __call__(self, email: str, password: str, address: Optional[str] = None) -> UserBO:
        if self.user_database.exists(user_email=email):
                    raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail="User already exists")
        current_new_user = UserBO(            
            email=email,
            hashed_password=compute_hash_password(email, password),
            address=address
        )
        self.user_database.create(user=current_new_user)

        return current_new_user