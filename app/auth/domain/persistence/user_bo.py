from abc import ABC, abstractmethod

from app.auth.domain.bo.user_bo import userBO


class UserBOPersistenceInterface(ABC):
    @abstractmethod
    async def get(self, email: str) -> userBO:
        pass

    @abstractmethod
    async def exists(self, user_email: str) -> bool:
        pass

    @abstractmethod
    async def create(self, user: userBO) -> userBO:
        pass