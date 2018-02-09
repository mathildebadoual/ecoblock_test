import sqlite3
import datetime
from datetime import datetime
import time
import os
import csv
import re

# irradiance to pv generation 920.79x + 46.378
reading_a = []
initial_time = []
timelapse = []

conn = sqlite3.connect('astrodek.sqlite')
cur = conn.cursor()

drop_table_ev_state = ("DROP TABLE IF EXISTS " +
            "[" + "pv_irradiance_data" + "]" )

create_table_ev_state = ("CREATE TABLE IF NOT EXISTS " +
            "[" + "pv_irradiance_data" + "]" +
            """ (id INTEGER PRIMARY KEY UNIQUE,
            simulation_id TEXT,
            simulation_num TEXT,
            origin TEXT,
            time TIME,
            hour TIME,
            irradiance FLOAT)""")

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
            # for j in reading_b:
            count = 1
            selected_id = []
            selected_values = []

            #Randomly select an id matching the input data from the
            #results.csv table
            sql_script =    ('''SELECT id FROM irradiance_raw
                             WHERE season = ? AND time = ?
                             ORDER BY RANDOM() LIMIT 1''')

            sql =   cur.execute(sql_script, (sim_season,
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
                sql_script =    ('''SELECT id, time, season,
                                irradiance  FROM irradiance_raw
                                WHERE id = ? LIMIT 1''')
                sql = cur.execute(sql_script, (i,))

                for row in sql:
                    selected_values.append(row)
            #
            for i in selected_values:
                sql_script = '''INSERT OR IGNORE INTO [pv_irradiance_data]
                                (simulation_id, simulation_num, origin,time,
                                hour, irradiance)
                                VALUES (?,?,?,?,?,?)'''
                sql = cur.execute(sql_script, (sim_id, simulation, i[0],
                      i[1], hourofday, i[3]))

                if hourofday < sim_timelapse:
                    hourofday += 1
                else:
                    hourofday = date_time.hour

            print "simulation done"

            simulation += 1

#commit and close
conn.commit()
conn.close()
