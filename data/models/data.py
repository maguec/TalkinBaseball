from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dataclasses import dataclass
import csv, glob

# Define the declarative base
Base = declarative_base()

class Player(Base):
    __tablename__ = 'players' # Define the table name in the database
    id = Column(Integer, primary_key=True) # Add a primary key column
    name_last = Column(String)
    name_first = Column(String)
    key_fangraphs = Column(Integer)
    mlb_played_first = Column(Integer)
    mlb_played_last = Column(Integer)

    def __init__(self, id, name_last, name_first, mlb_played_first, mlb_played_last, key_fangraphs):
        self.id = int(id)
        self.name_last = name_last
        self.name_first = name_first
        self.mlb_played_first = int(float(mlb_played_first))
        self.mlb_played_last = int(float(mlb_played_last))
        self.key_fangraphs = int(key_fangraphs)


@dataclass
class Players:
    players: list

    def __init__(self):
        self.players = []
        csvfiles = (glob.glob("../data/files/players.csv"))
        for csvfile in csvfiles:
            with open(csvfile) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.players.append(Player(
                        row['key_mlbam'], row['name_last'], row['name_first'], row['mlb_played_first'], row['mlb_played_last'], row['key_fangraphs']
                    ))

    def dbinit(self, engine):
        Base.metadata.create_all(engine)
    

class PitchAbbr(Base):
    __tablename__ = 'pitch_abbr' # Define the table name in the database
    id = Column(Integer, primary_key=True) # Add a primary key column
    pitch_type = Column(String)
    pitch_abbr = Column(String)

    def __init__(self, pitch_type, pitch_abbr):
        self.pitch_type = pitch_type
        self.pitch_abbr = pitch_abbr

@dataclass
class PitchAbbrs:
    pitches: list

    def __init__(self):
        self.pitches = []
        pitch_abbrs = [
            {'abbr': 'CH', 'pitch': 'Changeup'}, {'abbr': 'CS', 'pitch': 'SlowCurve'},
            {'abbr': 'CU', 'pitch': 'Curveball'}, {'abbr': 'EP', 'pitch': 'Eephus'},
            {'abbr': 'FA', 'pitch': 'Fastball'}, {'abbr': 'FC', 'pitch': 'Cutter'},
            {'abbr': 'FF', 'pitch': '4-Seam'}, {'abbr': 'FO', 'pitch': 'Forkball'},
            {'abbr': 'FS', 'pitch': 'Splitter'}, {'abbr': 'KC', 'pitch': 'KnuckleCurve'},
            {'abbr': 'KN', 'pitch': 'Knuckleball'}, {'abbr': 'PO', 'pitch': 'Pitchout'},
            {'abbr': 'SC', 'pitch': 'Screwball'}, {'abbr': 'SI', 'pitch': 'Sinker'},
            {'abbr': 'SL', 'pitch': 'Slider'}, {'abbr': 'ST', 'pitch': 'Sweeper'},
            {'abbr': 'SV', 'pitch': 'Slurve'}]
        for pitch in pitch_abbrs:
            self.pitches.append(PitchAbbr(pitch['pitch'], pitch['abbr']))

    def dbinit(self, engine):
        Base.metadata.create_all(engine)

class StatcastPitch(Base):
    __tablename__ = 'statcast_pitches' # Define the table name in the database

    # Define columns for each attribute
    id = Column(Integer, primary_key=True) # Add a primary key column
    pitch_type = Column(String)
    game_date = Column(DateTime)
    release_speed = Column(Float)
    batter = Column(Integer)
    pitcher = Column(Integer)
    balls = Column(Integer)
    strikes = Column(Integer)
    events = Column(String)
    outs_when_up = Column(Integer)
    inning = Column(Integer)
    pitch_number = Column(Integer)
    stand = Column(String)
    p_throws = Column(String)
    b_team = Column(String)
    p_team = Column(String)

    def __init__(self, game_date, pitch_type, release_speed, batter, pitcher, balls, strikes, outs_when_up, inning, pitch_number, events, stand,p_throws,b_team,p_team):
        self.pitch_type = pitch_type
        # Assuming game_date might come as a string, convert it to datetime object
        if isinstance(game_date, str):
            self.game_date = datetime.strptime(game_date, '%Y-%m-%d')
        else:
            self.game_date = game_date
        self.release_speed = release_speed
        self.batter = batter
        self.pitcher = pitcher
        self.balls = balls
        self.strikes = strikes
        self.outs_when_up = outs_when_up
        self.inning = inning
        self.pitch_number = pitch_number
        self.events = events
        self.stand = stand
        self.p_throws = p_throws
        self.b_team = b_team
        self.p_team = p_team

@dataclass
class StatcastPitches:
    pitches: list

    def __init__(self):
        self.pitches = []
        csvfiles = (glob.glob("../data/files/pitches.csv"))
        for csvfile in csvfiles:
            with open(csvfile) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        if row['inning_topbot'] == "Bot":
                            batter_team = row['home_team']
                            pitcher_team = row['away_team']
                        else:
                            batter_team = row['away_team']
                            pitcher_team = row['home_team']
                        self.pitches.append(StatcastPitch(
                            row['game_date'],
                            row['pitch_type'],
                            float(row['release_speed']),
                            int(row['batter']),
                            int(row['pitcher']),
                            int(row['balls']),
                            int(row['strikes']),
                            int(row['outs_when_up']),
                            int(row['inning']),
                            int(row['pitch_number']),
                            row['events'],
                            row['stand'],
                            row['p_throws'],
                            batter_team,
                            pitcher_team
                        ))
                    except Exception as e:
                        print("Error: ", e.__class__.__name__, row)

    def dbinit(self, engine):
        Base.metadata.create_all(engine)
