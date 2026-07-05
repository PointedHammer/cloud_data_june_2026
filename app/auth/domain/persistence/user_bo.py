from abc import ABC, abstractmethod

from app.auth.domain.bo.user_bo import userBO


class UserBOPersistenceInterface(ABC):
    @abstractmethod
    def get(self, email: str) -> userBO:
        pass

    @abstractmethod
    def exists(self, user_email: str) -> bool:
        pass

    @abstractmethod
    def create(self, user: userBO) -> userBO:
        pass