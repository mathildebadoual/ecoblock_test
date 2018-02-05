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


spring_start = '1/03/16 00:00.01'
spring_start_current = '1/03/17 00:00.01'
datetime_spring_start = (datetime.strptime(spring_start, '%d/%m/%y %H:%M.%S'))
ut_spring_start = (datetime_spring_start - dtt.datetime(1970, 1, 1)).total_seconds()
datetime_spring_start_current = (datetime.strptime(spring_start_current, '%d/%m/%y %H:%M.%S'))
ut_spring_start_current = (datetime_spring_start_current - dtt.datetime(1970, 1, 1)).total_seconds()

spring_end = '31/05/16 23:59.59'
spring_end_current = '31/05/17 23:59.59'
datetime_spring_end = (datetime.strptime(spring_end, '%d/%m/%y %H:%M.%S'))
ut_spring_end = (datetime_spring_end - dtt.datetime(1970, 1, 1)).total_seconds()
datetime_spring_end_current = (datetime.strptime(spring_end_current, '%d/%m/%y %H:%M.%S'))
ut_spring_end_current = (datetime_spring_end_current - dtt.datetime(1970, 1, 1)).total_seconds()

summer_start = '1/05/16 00:00.01'
summer_start_current = '1/05/17 00:00.01'
datetime_summer_start = (datetime.strptime(summer_start, '%d/%m/%y %H:%M.%S'))
ut_summer_start = (datetime_summer_start - dtt.datetime(1970, 1, 1)).total_seconds()
datetime_summer_start_current = (datetime.strptime(summer_start_current, '%d/%m/%y %H:%M.%S'))
ut_summer_start_current = (datetime_summer_start_current - dtt.datetime(1970, 1, 1)).total_seconds()

summer_end = '31/08/16 23:59.59'
summer_end_current = '31/08/17 23:59.59'
datetime_summer_end = (datetime.strptime(summer_end, '%d/%m/%y %H:%M.%S'))
ut_summer_end = (datetime_summer_end - dtt.datetime(1970, 1, 1)).total_seconds()
datetime_summer_end_current = (datetime.strptime(summer_end_current, '%d/%m/%y %H:%M.%S'))
ut_summer_end_current = (datetime_summer_end_current - dtt.datetime(1970, 1, 1)).total_seconds()

fall_start = '1/09/16 00:00.01'
fall_start_current = '1/09/17 00:00.01'
datetime_fall_start = (datetime.strptime(fall_start, '%d/%m/%y %H:%M.%S'))
ut_fall_start = (datetime_fall_start - dtt.datetime(1970, 1, 1)).total_seconds()
datetime_fall_start_current = (datetime.strptime(fall_start_current, '%d/%m/%y %H:%M.%S'))
ut_fall_start_current = (datetime_fall_start_current - dtt.datetime(1970, 1, 1)).total_seconds()

fall_end = '30/11/16 23:59.59'
fall_end_current = '30/11/17 23:59.59'
datetime_fall_end = (datetime.strptime(fall_end, '%d/%m/%y %H:%M.%S'))
ut_fall_end = (datetime_fall_end - dtt.datetime(1970, 1, 1)).total_seconds()
datetime_fall_end_current = (datetime.strptime(fall_end_current, '%d/%m/%y %H:%M.%S'))
ut_fall_end_current = (datetime_fall_end_current - dtt.datetime(1970, 1, 1)).total_seconds()

winter_start_late = '1/12/16 00:00.01'
winter_start_late_current = '1/12/17 00:00.01'
datetime_winter_start_late = (datetime.strptime(winter_start_late, '%d/%m/%y %H:%M.%S'))
ut_winter_start_late = (datetime_winter_start_late - dtt.datetime(1970, 1, 1)).total_seconds()
datetime_winter_start_late_current = (datetime.strptime(winter_start_late_current, '%d/%m/%y %H:%M.%S'))
ut_winter_start_late_current = (datetime_winter_start_late_current - dtt.datetime(1970, 1, 1)).total_seconds()

winter_end_late = '31/12/16 23:59.59'
winter_end_late_current = '31/12/17 23:59.59'
datetime_winter_end_late = (datetime.strptime(winter_end_late, '%d/%m/%y %H:%M.%S'))
ut_winter_end_late = (datetime_winter_end_late - dtt.datetime(1970, 1, 1)).total_seconds()
datetime_winter_end_late_current = (datetime.strptime(winter_end_late_current, '%d/%m/%y %H:%M.%S'))
ut_winter_end_late_current = (datetime_winter_end_late_current - dtt.datetime(1970, 1, 1)).total_seconds()

winter_start_early = '1/01/16 00:00.01'
winter_start_early_current = '1/01/17 00:00.01'
datetime_winter_start_early = (datetime.strptime(winter_start_early, '%d/%m/%y %H:%M.%S'))
ut_winter_start_early = (datetime_winter_start_early - dtt.datetime(1970, 1, 1)).total_seconds()
datetime_winter_start_early_current = (datetime.strptime(winter_start_early_current, '%d/%m/%y %H:%M.%S'))
ut_winter_start_early_current = (datetime_winter_start_early_current - dtt.datetime(1970, 1, 1)).total_seconds()

winter_end_early = '28/02/16 23:59.59'
winter_end_early_current = '28/02/17 23:59.59'
datetime_winter_end_early = (datetime.strptime(winter_end_early, '%d/%m/%y %H:%M.%S'))
ut_winter_end_early = (datetime_winter_end_early - dtt.datetime(1970, 1, 1)).total_seconds()
datetime_winter_end_early_current = (datetime.strptime(winter_end_early_current, '%d/%m/%y %H:%M.%S'))
ut_winter_end_early_current = (datetime_winter_end_early_current - dtt.datetime(1970, 1, 1)).total_seconds()


conn = sqlite3.connect('astrodek.sqlite')
cur = conn.cursor()

drop_table_ev_raw = ("DROP TABLE IF EXISTS" +
            "[" + "ev_raw" + "]")

create_table_ev_raw = ("CREATE TABLE IF NOT EXISTS " +
            "[" + "ev_raw" + "]" +
            """ (id INTEGER PRIMARY KEY UNIQUE,
            reading TEXT,
            date DATE,
            day INTEGER,
            time TIME,
            timestamp TIMESTAMP,
            season TEXT,
            load_demand FLOAT,
            charging BOOLEAN)""")

cur.execute(drop_table_ev_raw)
cur.execute(create_table_ev_raw)

d = os.getcwd()

d1 = os.path.join(d,'Data')
fname = os.path.join(d1,'pecan_cars.csv')


with open(fname, 'rU') as main_data_csv:
    main_data_reader = csv.DictReader(main_data_csv)
    for i in main_data_reader:
        dataid = str(i['dataid'])
        date_reading = str(i['localminute'])
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
