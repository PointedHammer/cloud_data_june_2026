


from dependency_injector import containers, providers


from ...persistence.memory_database.user_bo import UserBOMemoryPersistence



class UserBOPersistences(containers.DeclarativeContainer):

    memory = providers.Singleton(

        UserBOMemoryPersistence,

    )