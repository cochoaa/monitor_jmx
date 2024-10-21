from sqlalchemy import create_engine,and_,or_
from sqlalchemy.orm import sessionmaker
class Datasource():
    def __init__(self,user:str,password:str,host:str,port:str,name:str,timeout:int=10):
        args = {'connect_timeout': timeout}
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{name}',connect_args=args)
        self.engine = engine
        self.Session = sessionmaker(engine)