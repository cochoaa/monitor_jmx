from datetime import datetime
from model.memory import Memory
from typing import List
from repository.memory_repository import MemoryRepository


class MemoryService:
    def __init__(self, memoryRepository: MemoryRepository):
        self.memoryRepository = memoryRepository

    def check(self):
        check = self.memoryRepository.check()
        return check

    def __convert_to_memory(self, mem: dict) -> Memory:
        return Memory(
            time=mem.get("time"),
            name=mem.get("name"),
            value=mem.get("value")
        )

    def __converto_to_list_memory(self, list_dict) -> List[Memory]:
        memories = []
        for mem in list_dict:
            memories.append(self.__convert_to_memory(mem))
        return memories

    def save(self, list_dict):
        list_memories = self.__converto_to_list_memory(list_dict)
        self.memoryRepository.save(list_memories)
