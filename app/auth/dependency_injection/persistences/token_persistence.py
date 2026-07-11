from app.auth.dependency_injector import containers, providers
from app.auth.persistence.memory.token import TokenMemoryPersistenceService
from app.auth.persistence.redis.token import TokenRedisPersistenceService


class TokenPersistence(containers.DeclarativeContainer):
    memory = providers.Singleton(TokenMemoryPersistenceService)

    redis = providers.Singleton(TokenRedisPersistenceService)



    carlemany = redis 