from abc import ABC, abstractmethod

from app.auth.domain.bo.user_bo import userBO



class TokenBOPersistenceInterface(ABC):
    @abstractmethod
    def get(self, token: str) -> str:
        pass


    @abstractmethod
    def generate_token(self, email: str) -> str:
        pass