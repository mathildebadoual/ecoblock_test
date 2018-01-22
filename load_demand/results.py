import sqlite3
import datetime
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
                        demand FLOAT)""")

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
        date_time = (datetime.strptime(sim_starttime, '%H:%M:%S'))
        sim_timelapse = int(i['hours'])
        timelapse.append(sim_timelapse)
        sim_numof = int(i['simulations'])
        simulation = 1
        while simulation < sim_numof + 1:
            count = 0
            hour = 1
            while count < sim_timelapse:
                timeofday = str(date_time.time())
                sql_script = 'SELECT SUM (load_demand) FROM data_results WHERE hour = ? AND simulation_id = ? AND simulation_num = ?'
                load_sum = cur.execute(sql_script, (hour, sim_id, simulation))
                for i in load_sum:
                    load = i[0]
                    print load
                    sql_script = '''INSERT OR IGNORE INTO [results]
                                    (time, demand, simulation_id, simulation_num) VALUES (?,?,?,?)'''
                    sql = cur.execute(sql_script, (timeofday,load, sim_id, simulation))

                date_time = date_time + timedelta(minutes = 60)
                count += 1
                hour += 1
            simulation += 1

conn.commit()
conn.close()
