import csv
import sqlite3
import re
import dateutil.parser as parser
import os
import pytz
import time
from datetime import datetime
from datetime import timedelta
import datetime as dtt
from datetime import date


conn = sqlite3.connect('astrodek.sqlite')
cur = conn.cursor()

drop_table_ev_raw = ("DROP TABLE IF EXISTS" +
            "[" + "irradiance_ev_raw" + "]")

create_table_ev_raw = ("CREATE TABLE IF NOT EXISTS " +
            "[" + "irradiance_ev_raw" + "]" +
            """ (id INTEGER PRIMARY KEY UNIQUE,
            irradiance INTEGER,
            pv_generation FLOAT)""")

cur.execute(drop_table_ev_raw)
cur.execute(create_table_ev_raw)

d = os.getcwd()

d1 = os.path.join(d,'Data')
fname = os.path.join(d1,'irradiance_pv.csv')


with open(fname, 'rU') as main_data_csv:
    main_data_reader = csv.DictReader(main_data_csv)
    for i in main_data_reader:
        irradiance_values = str(i['irradiance'])
        power_values = str(i['power'])
        sql_script = ('INSERT INTO' + '[' + 'irradiance_ev_raw' + ']' +
        '(irradiance, pv_generation) VALUES ' + '(' + '?' + ',' + '?' + ')')

        cur.execute(sql_script,(irradiance_values,power_values))

conn.commit()
conn.close()
