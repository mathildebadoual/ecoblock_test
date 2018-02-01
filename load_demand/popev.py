import sqlite3
import datetime
from datetime import datetime
import time
import os
import csv
import re

reading_a = []
reading_b = ['vehicle1', 'vehicle2', 'vehicle3', 'vehicle4', 'vehicle5',
            'vehicle6', 'vehicle7', 'vehicle8', 'vehicle9', 'vehicle10',
            'vehicle11', 'vehicle12', 'vehicle13', 'vehicle14', 'vehicle15',
            'vehicle16', 'vehicle17', 'vehicle18', 'vehicle19', 'vehicle20',
            'vehicle21', 'vehicle22', 'vehicle23', 'vehicle24']
initial_time = []
timelapse = []

conn = sqlite3.connect('astrodek.sqlite')
cur = conn.cursor()

drop_table_ev_state = ("DROP TABLE IF EXISTS " +
            "[" + "ev_state" + "]" )

create_table_ev_state = ("CREATE TABLE IF NOT EXISTS " +
            "[" + "ev_state" + "]" +
            """ (id INTEGER PRIMARY KEY UNIQUE,
            simulation_id TEXT,
            simulation_num TEXT,
            origin TEXT,
            time TIME,
            hour TIME,
            vehicle TEXT,
            load_demand FLOAT,
            charging BOOLEAN)""")

cur.execute(drop_table_ev_state)
cur.execute(create_table_ev_state)

d = os.getcwd()

d1 = os.path.join(d,'Data')
fname = os.path.join(d1,'results.csv')


with open(fname, 'rU') as main_data_csv:
    main_data_reader = csv.DictReader(main_data_csv)
    for i in main_data_reader:
        sim_id = i['id']
        sim_startday = int(i['start_day'])
        sim_starttime = str(i['start_time'])
        date_time = (datetime.strptime(sim_starttime, '%H:%M:%S'))
        timeofday = str(date_time.time())
        hourofday = date_time.hour
        initial_time.append(timeofday)
        sim_timelapse = int(i['hours'])
        timelapse.append(sim_timelapse)
        sim_numof = int(i['simulations'])
        sim_season = i['season']
        simulation = 1
        while simulation < sim_numof + 1:
            hourofday = date_time.hour

            #run through the vehicle list to create a profile for each vehicle
            for j in reading_b:
                vehicle = j
                count = 1
                selected_id = []
                selected_values = []

                #Randomly select an id matching the input data from the
                #results.csv table
                sql_script =    ('''SELECT id FROM ev_raw
                                 WHERE day = ? AND season = ? AND time = ?
                                 ORDER BY RANDOM() LIMIT 1''')

                sql =   cur.execute(sql_script, (sim_startday, sim_season,
                        timeofday))

                # Store selected ids
                for row in sql:
                    selected_id.append(row[0])
                sl_id = selected_id[0]

                # For each of the selected ids select the next in the sequence
                # to generate the ids that will create the time lapse specified
                while count < sim_timelapse:
                    sl_id += 1
                    selected_id.append(sl_id)
                    count += 1

                #for each id in the list, select the required values and insert
                #them into the ev_state table
                for i in selected_id:
                    sql_script =    ('''SELECT id, day, time, season,
                                    load_demand, charging  FROM ev_raw
                                    WHERE id = ? LIMIT 1''')
                    sql = cur.execute(sql_script, (i,))

                    for row in sql:
                        selected_values.append(row)

                for i in selected_values:
                    sql_script = '''INSERT OR IGNORE INTO [ev_state]
                                    (simulation_id, simulation_num, origin,time,
                                    vehicle, hour, load_demand, charging)
                                    VALUES (?,?,?,?,?,?,?,?)'''
                    sql = cur.execute(sql_script, (sim_id, simulation, i[0],
                          i[2], vehicle, hourofday, i[4], i[5]))
                    if hourofday < sim_timelapse:
                        hourofday += 1
                    else:
                        hourofday = date_time.hour

                print "simulation done"

            simulation += 1

#commit and close
conn.commit()
conn.close()
