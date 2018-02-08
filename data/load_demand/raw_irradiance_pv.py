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
            "[" + "ev_raw" + "]" +
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
        dataid = str(i['irradiance'])
        date_reading = str(i['power'])
        load_demand = float(i['car1'])
        date_time = (datetime.strptime(date_reading, '%m/%d/%y %H:%M'))
        datetime_adjusted = date_time + timedelta(minutes = 59)
        ut = (datetime_adjusted - dtt.datetime(1970, 1, 1)).total_seconds()
        day = date_time.weekday()
        onlytime = str(datetime_adjusted.time())

        if ((ut > ut_spring_start and ut < ut_spring_end) or
            (ut > ut_spring_start_current and ut < ut_spring_end_current)):
            season = 'spring'
        elif ((ut > ut_summer_start and ut < ut_summer_end) or
            (ut > ut_summer_start_current and ut < ut_summer_end_current)):
            season = 'summer'
        elif ((ut > ut_fall_start and ut < ut_fall_end) or
            (ut > ut_fall_start_current and ut < ut_fall_end_current)):
            season = 'fall'
        elif ((ut > ut_winter_start_late and ut < ut_winter_end_late) or
            (ut > ut_winter_start_early and ut < ut_winter_end_early)):
            season = 'winter'
        elif ((ut > ut_winter_start_late_current and
            ut < ut_winter_end_late_current) or
            (ut > ut_winter_start_early_current and
            ut < ut_winter_end_early_current)):
            season = 'winter'
        else:
            print 'error producing season'

        if load_demand > .01:
            charging_state = True
        else:
            charging_state = False

        sql_script = ('INSERT INTO' + '[' + 'ev_raw' + ']' +
        '(reading, date, day, time, timestamp, season, load_demand, charging) VALUES ' +
        '(' + '?' + ',' + '?' + ',' + '?' + ',' + '?' + ',' + '?' + ',' + '?' + ',' + '?' + ',' + '?' + ')')

        cur.execute(sql_script,(dataid, datetime_adjusted, day, onlytime, ut, season, load_demand, charging_state))

conn.commit()
conn.close()
