import sqlite3
import datetime as dtt
from datetime import datetime
from datetime import timedelta
import time
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.dates import DateFormatter, HourLocator, MinuteLocator


weekdaytonumber = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3,
                'Friday':4, 'Saturday':5, 'Sunday':6}

reading_a = []
reading_b = ['building1', 'building2', 'building3', 'building4', 'building5',
            'building6', 'building7', 'building8', 'building9', 'building10',
            'building11', 'building12', 'building13', 'house']
reading_c = ['building2', 'building5', 'building6', 'building11']
initial_time = []
timelapse = []

#connect to database
conn = sqlite3.connect('astrodek.sqlite')
cur = conn.cursor()

drop_table_results =   ("DROP TABLE IF EXISTS " + "[" + "results" + "]" )

create_table_results = ("CREATE TABLE IF NOT EXISTS " +
                        "[" + "results" + "]" +
                        """ (id INTEGER PRIMARY KEY UNIQUE,
                        simulation_id INTEGER,
                        simulation_num INTEGER,
                        time TIME,
                        timestamp TIMESTAMP,
                        demand FLOAT,
                        ev_demand FLOAT)""")

cur.execute(drop_table_results)
cur.execute(create_table_results)

#empty list with randomly selected points

d = os.getcwd()

d1 = os.path.join(d,'Data')
fname = os.path.join(d1,'results.csv')


with open(fname, 'rU') as main_data_csv:
    main_data_reader = csv.DictReader(main_data_csv)
    for i in main_data_reader:
        sim_id = i['id']
        sim_starttime = str(i['start_time'])
        season = str(i['season'])

        if season == 'winter':
            sim_starttime = "01/01/17 "+str(i['start_time'])
            date_time = (datetime.strptime(sim_starttime, '%d/%m/%y %H:%M:%S'))

        elif season == 'spring':
            sim_starttime = "01/03/17 "+str(i['start_time'])
            date_time = (datetime.strptime(sim_starttime, '%d/%m/%y %H:%M:%S'))

        elif season == 'summer':
            sim_starttime = "01/05/17 "+str(i['start_time'])
            date_time = (datetime.strptime(sim_starttime, '%d/%m/%y %H:%M:%S'))

        elif season == 'fall':
            sim_starttime = "01/09/17 "+str(i['start_time'])
            date_time = (datetime.strptime(sim_starttime, '%d/%m/%y %H:%M:%S'))

        sim_timelapse = int(i['hours'])
        timelapse.append(sim_timelapse)
        sim_numof = int(i['simulations'])
        season = str(i['season'])
        simulation = 1
        print sim_timelapse
        while simulation < sim_numof + 1:
            count = 0
            hour = 1
            while count < sim_timelapse:
                ut_time = (date_time - dtt.datetime(1970, 1, 1)).total_seconds()
                ev_load = 0
                timeofday = str(date_time.time())

                sql_ev_script = 'SELECT SUM (load_demand) FROM ev_state WHERE hour = ? AND simulation_id = ? AND simulation_num = ?'
                ev_load_sum = cur.execute(sql_ev_script, (hour, sim_id, simulation))
                for row in ev_load_sum:
                    ev_load = row[0]

                sql_script = 'SELECT SUM (load_demand) FROM data_results WHERE hour = ? AND simulation_id = ? AND simulation_num = ?'
                load_sum = cur.execute(sql_script, (hour, sim_id, simulation))

                for i in load_sum:
                    load = i[0]
                    sql_script = '''INSERT OR IGNORE INTO [results]
                                    (time, demand, simulation_id, simulation_num, ev_demand, timestamp) VALUES (?,?,?,?,?,?)'''
                    sql = cur.execute(sql_script, (timeofday,load, sim_id, simulation, ev_load,ut_time))

                date_time = date_time + timedelta(minutes = 60)
                count += 1
                hour += 1
            simulation += 1

conn.commit()
conn.close()
