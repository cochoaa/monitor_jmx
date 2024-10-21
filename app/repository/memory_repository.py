from repository.datasource import Datasource
from datetime import datetime
from model.memory import Memory
from typing import List


class MemoryRepository:
    def __init__(self, datasource: Datasource):
        self.Session = datasource.Session

    def check(self):
        try:
            with self.Session.begin() as session:
                session.query(Memory) \
                    .filter(Memory.time < datetime.now()) \
                    .first()
            return True
        except Exception as e:
            print(e)
            return False

    def save(self, memories: List[Memory]):
        with self.Session.begin() as session:
            session.add_all(memories)
