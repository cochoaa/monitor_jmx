from dependency_injector import containers, providers
from repository.datasource import Datasource

class Container(containers.DeclarativeContainer):
    config = providers.Configuration(strict=True)
    datasource = providers.Singleton(
        Datasource,
        user=config.db.user,
        password=config.db.password,
        host=config.db.host,
        port=config.db.port,
        name=config.db.name
    )


