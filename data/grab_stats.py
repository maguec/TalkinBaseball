#!/usr/bin/env python3

from pybaseball import statcast

import warnings

warnings.filterwarnings("ignore")

data = statcast("2025-04-01", "2025-08-03")
data.to_csv("./files/pitches.csv")
