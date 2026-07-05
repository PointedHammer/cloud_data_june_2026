


from dependency_injector import containers, providers


from app.auth.domain.controllers.post_register import PostRegisterController
from app.auth.persistence.memory.user_bo import UserBoMemoryPersistenceService



class RegisterControllers(containers.DeclarativeContainer):

    carlemany = providers.Singleton(

        PostRegisterController,
        user_database=UserBoMemoryPersistences.memory,
    )