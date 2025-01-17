from datetime import datetime, timezone
from jmxquery import JMXConnection, JMXQuery
from typing import List


class JMXRepository:
    def __init__(self, host: str, port: int, user: str = None, password: str = None):
        self.user = user
        self.password = password
        self.host = host
        jmx_url = f'service:jmx:rmi:///jndi/rmi://{host}:{port}/jmxrmi'
        self.jmx_queries = [
            JMXQuery("java.lang:type=Memory"),
            JMXQuery("java.lang:type=MemoryPool,name=*Eden Space/Usage",),
            JMXQuery("java.lang:type=MemoryPool,name=*Old Gen/Usage"),
            JMXQuery("java.lang:type=MemoryPool,name=*Survivor Space/Usage"),
            JMXQuery("java.lang:type=MemoryPool,name=Tenured Gen/Usage"),
            JMXQuery("java.lang:type=MemoryPool,name=Code Cache/Usage"),
            JMXQuery("java.lang:type=MemoryPool,name=Metaspace/Usage"),
            JMXQuery("java.lang:type=MemoryPool,name=Compressed Class Space/Usage")
        ]
        self.jmx_conn = JMXConnection(jmx_url)

    def check(self):
        try:
            metrics = self.list_memory()
            return len(metrics)>0
        except Exception as e:
            print(e)
            return False

    def list_memory(self) -> List[dict]:
        try:
            list_dict = []
            timestamp = datetime.now(timezone.utc)
            metrics = self.jmx_conn.query(self.jmx_queries)
            metrics = list(filter(lambda m: m.attributeKey == 'used', metrics))
            for metric in metrics:
                name = metric.mBeanName.replace("java.lang:type=", "")
                name = name.replace("MemoryPool,name=", "")
                name = metric.attribute if name == 'Memory' else name
                metric_dict = {
                    'time': timestamp,
                    'name': name,
                    'value': metric.value,
                    'server': self.host,
                }
                list_dict.append(metric_dict)
            return list_dict
        except Exception as e:
            print(e)
            return []
