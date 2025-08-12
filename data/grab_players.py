#!/usr/bin/env python3

from pybaseball import playerid_reverse_lookup
from models.data import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, text
import os
import pandas as pd

def chunker(myset, size):
    s = sorted(myset)
    for i in range(0, len(s), size):
        yield s[i:i+size]

def get_player_id(player_id):
    return playerid_reverse_lookup(player_id)

def get_players(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    player_ids = set()
    q1 = "SELECT DISTINCT(pitcher) FROM statcast_pitches"
    result = session.execute(text(q1))
    for row in result:
        player_ids.add(row[0])
    q2 = "SELECT distinct(batter) FROM statcast_pitches"
    result = session.execute(text(q2))
    for row in result:
        player_ids.add(row[0])
    return chunker(player_ids, 50)

if __name__ == '__main__':
    if os.getenv('DATABASE_URL'):
        engine = create_engine(os.getenv('DATABASE_URL'))
    else:
        engine = create_engine('sqlite:///pitches.db')
    players = get_players(engine)
    myframe = pd.DataFrame()
    for chunk in players:
        myframe = pd.concat([myframe, pd.DataFrame(get_player_id(chunk))], ignore_index=True)
    myframe.to_csv('./files/players.csv')


