from models.data import *
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os


def load_data(Session, engine):
    session = Session()
    players = Players()
    players.dbinit(engine)
    session.add_all(players.players)
    session.commit()


if __name__ == '__main__':
    if os.getenv('DATABASE_URL'):
        engine = create_engine(os.getenv('DATABASE_URL'))
    else:
        engine = create_engine('sqlite:///pitches.db')
    Base = declarative_base()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    load_data(Session, engine) 



