import sqlite3
import datetime
from datetime import datetime
import time
import os
import csv
import re

fleet_size = int(input ("Number of vehicles (n) = "))

conn = sqlite3.connect('astrodek.sqlite')
cur = conn.cursor()

drop_table_ev_state = ("DROP TABLE IF EXISTS " +
            "[" + "ev_state" + "]" )

create_table_ev_state = ("CREATE TABLE IF NOT EXISTS " +
            "[" + "ev_state" + "]" +
            """ (id INTEGER PRIMARY KEY UNIQUE,
            time TIME,
            vehicle1 TEXT, vehicle2 TEXT, vehicle3 TEXT, vehicle4 TEXT,
            vehicle5 TEXT, vehicle6 TEXT, vehicle7 TEXT, vehicle8 TEXT,
            vehicle9 TEXT, vehicle10 TEXT, vehicle11 TEXT, vehicle12 TEXT,
            vehicle13 TEXT, vehicle14 TEXT, vehicle15 TEXT, vehicle16 TEXT,
            vehicle17 TEXT, vehicle18 TEXT, vehicle19 TEXT, vehicle20 TEXT,
            vehicle21 TEXT, vehicle22 TEXT, vehicle23 TEXT, vehicle24 TEXT,
            load_demand FLOAT,
            scenario TEXT)""")
