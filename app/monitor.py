from service.jmx_service import JMXService
from config import log_config
from service.memory_service import MemoryService

logger = log_config.getLogger()


class Monitor:
    def __init__(self,
                 jmxService: JMXService,
                 memoryService: MemoryService):
        self.jmxService = jmxService
        self.memoryService = memoryService

    def check(self):
        try:
            if self.jmxService.check():
                logger.info("JMX Check: Conexion Correcta")
            else:
                logger.error("JMX Check: Conexion Fallida")

            if self.memoryService.check():
                logger.info("BD Check: Conexion Correcta")
            else:
                logger.error("BD Check: Conexion Fallida")
        except Exception as e:
            logger.error(e)
