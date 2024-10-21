from service.jmx_service import JMXService
from config import log_config
logger=log_config.getLogger()
class Monitor():
    def __init__(self, jmxService: JMXService):
        self.jmxService = jmxService

    def check(self):
        try:
            jmxService=self.jmxService
            if jmxService.check_Origin():
                logger.info("Monitor Check: Conexion Correcta al Servidor Origin")
            else:
                logger.info("Monitor Check: Conexion Fallida al Servidor Origin")

            if serviceSession.check_Monitor():
                logger.info("Monitor Check: Conexion Correcta al Servidor Monitor")
            else:
                logger.info("Monitor Check: Conexion Fallida al Servidor Monitor")
        except:
            logger.error("Monitor Check: Conexion Fallida al Servidor Origin y Monitor")