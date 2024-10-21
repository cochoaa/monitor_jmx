import time
from jmxquery import JMXConnection, JMXQuery

# Configuración de JMX
jmx_host = 'chancay.unmsm.edu.pe'
jmx_port = '9999'
jmx_url = f'service:jmx:rmi:///jndi/rmi://{jmx_host}:{jmx_port}/jmxrmi'
queries = [
    JMXQuery("java.lang:type=Memory"),
    JMXQuery("java.lang:type=MemoryPool,name=PS Eden Space/Usage"),
    JMXQuery("java.lang:type=MemoryPool,name=PS Old Gen/Usage"),
    JMXQuery("java.lang:type=MemoryPool,name=PS Survivor Space/Usage"),
    JMXQuery("java.lang:type=MemoryPool,name=Code Cache/Usage"),
    JMXQuery("java.lang:type=MemoryPool,name=Metaspace/Usage"),
    JMXQuery("java.lang:type=MemoryPool,name=Compressed Class Space/Usage")
]
jmx_query = 'java.lang:type=Memory'

monitoring_interval = 2

try:
    # Establecer la conexión JMX
    jmx_conn = JMXConnection(jmx_url)
    while True:
        # Consultar el uso de memoria
        metrics = jmx_conn.query(queries)
        metrics = list(filter(lambda metric: metric.attributeKey == 'used', metrics))
        for metric in metrics:
            name = metric.mBeanName.replace("java.lang:type=", "")
            name = name.replace("MemoryPool,name=", "")
            attribute = metric.attribute
            name = attribute if name =='Memory' else name
            print(f"{name}  ({metric.value_type}) = {metric.value} {metric.attributeKey}")
        # Esperar el intervalo de monitoreo
        time.sleep(monitoring_interval)

except KeyboardInterrupt:
    print("Monitoreo detenido.")


