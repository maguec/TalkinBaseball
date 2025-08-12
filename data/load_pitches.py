from models.data import *
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os


def load_data(Session, engine):
    session = Session()
    pitches = StatcastPitches()
    pitches.dbinit(engine)
    session.add_all(pitches.pitches)
    try:
        session.commit()
    except Exception as e:
        print("Error: ", e.__class__.__name__, e)
    session.close()


if __name__ == '__main__':
    if os.getenv('DATABASE_URL'):
        engine = create_engine(os.getenv('DATABASE_URL'))
    else:
        engine = create_engine('sqlite:///pitches.db')
    Base = declarative_base()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    load_data(Session, engine) 



