import os
from sqlalchemy import create_engine, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column 



Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    user_id = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})"

# Define your SQLAlchemy engine and create the tables as needed
