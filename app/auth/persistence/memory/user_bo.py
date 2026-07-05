from abc import ABC, abstractmethod

from app.auth.domain.bo.user_bo import userBO
from app.auth.domain.persistence.user_bo import UserBOPersistenceInterface


class UserBoMemoryPersistenceService(UserBOPersistenceInterface):
    
    def __init__(self):
        self.user_database = {}

    def get(self, email: str) -> userBO:
        return self.user_database[email]

    def exists(self, user_email: str) -> bool:
        return user_email in self.user_database

    
    def create(self, user: userBO) -> userBO:
        self.user_database[user.email] = user
        return user