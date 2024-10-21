from dependency_injector import containers, providers
from repository.datasource import Datasource
from repository.jmx_repository import JMXRepository
from repository.memory_repository import MemoryRepository
from service.jmx_service import JMXService
from service.memory_service import MemoryService


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
    jmxRepository = providers.Singleton(
        JMXRepository,
        host=config.jmx.host,
        port=config.jmx.port,
    )

    memoryRepository = providers.Singleton(
        MemoryRepository,
        datasource=datasource
    )

    jmxService = providers.Singleton(
        JMXService,
        jmxRepository=jmxRepository
    )

    memoryService = providers.Singleton(
        MemoryService,
        memoryRepository=memoryRepository
    )

