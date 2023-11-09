import os
from sqlalchemy import create_engine, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.orm import sessionmaker, Session
from .models import Base
current_directory = os.getcwd()
db_path = f'sqlite:///database/users.sqlite3'
engine = create_engine(db_path,connect_args={'check_same_thread': False})


# Create the tables in the database
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        #print('closing')
        db.close()
