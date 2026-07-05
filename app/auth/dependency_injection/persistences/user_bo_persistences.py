


from dependency_injector import containers, providers


from app.auth.persistence.memory.user_bo import UserBoMemoryPersistenceService



class UserBOPersistences(containers.DeclarativeContainer):

    memory = providers.Singleton(

        UserBoMemoryPersistenceService,
    )

    carlemany =  memory