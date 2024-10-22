from sqlalchemy import Column
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy import DateTime
from model.base import Base

class Memory(Base):
    __tablename__ = 'htb_memory'
    name = Column(String)
    value = Column(BigInteger)
    time = Column(DateTime,primary_key=True)