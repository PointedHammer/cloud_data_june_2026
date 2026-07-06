


from dependency_injector import containers, providers


from app.auth.domain.controllers.post_register import PostRegisterController
from app.auth.dependency_injection.persistences.user_bo_persistences import UserBOPersistences
from app.auth.domain.persistence.token_persistence import TokenPersistences



class PostRegisterControllers(containers.DeclarativeContainer):

    carlemany = providers.Singleton(

        PostRegisterController,
        user_database=UserBOPersistences.carlemany(),
        token_database=TokenPersistences.carlemany()
    )