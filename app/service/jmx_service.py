from config import log_config
from repository.jmx_repository import JMXRepository

logger = log_config.getLogger()


class JMXService:
    def __init__(self, jmxRepository: JMXRepository):
        self.jmxRepository = jmxRepository

    def check(self):
        check = self.jmxRepository.check()
        return check

    def read(self):
        memories = self.jmxRepository.list_memory()
        return memories


if __name__ == "__main__":
    host = "chancay.unmsm.edu.pe"
    port = 9999
    repository = JMXRepository(host=host, port=port)
    service = JMXService(repository)
    memories = service.read()
    for mem in memories:
        print(mem)
