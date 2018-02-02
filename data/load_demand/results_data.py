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

drop_table_data_results =   ("DROP TABLE IF EXISTS " +
                            "[" + "data_results" + "]" )

create_table_data_results = ("CREATE TABLE IF NOT EXISTS " +
                            "[" + "data_results" + "]" +
                            """ (id INTEGER PRIMARY KEY UNIQUE,
                            building TEXT,
                            simulation_id INTEGER,
                            simulation_num INTEGER,
                            time DATETIME,
                            hour INTEGER,
                            origin1 TEXT,
                            origin2 TEXT,
                            origin3 TEXT,
                            origin4 TEXT,
                            load_demand FLOAT) """)

cur.execute(drop_table_data_results)
cur.execute(create_table_data_results)

#empty list with randomly selected points

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
        initial_time.append(timeofday)
        sim_timelapse = int(i['hours'])
        timelapse.append(sim_timelapse)
        sim_numof = int(i['simulations'])
        sim_season = i['season']
        simulation = 1
        while simulation < sim_numof + 1:
            count = 0
            hour = 1
            while count < sim_timelapse:
                timeofday = str(date_time.time())
                for j in reading_b:
                    if j == "building1":
                        lodem = []
                        building_id = []
                        for k in reading_c:
                            sql_script =    ('''SELECT demand_building, id FROM eb_data_clean
                                            WHERE day =? AND season = ? AND time = ?
                                            AND building = ? ORDER BY RANDOM()
                                            LIMIT 1''')
                            sql = cur.execute(sql_script, (sim_startday, sim_season,
                                  timeofday, k))
                            for row in sql:
                                lodem.append(row[0])
                                building_id.append(row[1])

                        total_demand = sum(lodem)/4
                        sql_script = '''INSERT OR IGNORE INTO [data_results]
                                        (load_demand, time, origin1, origin2,
                                        origin3, origin4, building, simulation_id, hour, simulation_num) VALUES (?,?,?,?,?,?, 'building1',?,?,?)'''
                        sql = cur.execute(sql_script, (total_demand,timeofday,
                              building_id[0], building_id[1], building_id[2], building_id[3], sim_id, hour, simulation))

                    elif j == "building3":
                        lodem = []
                        building_id = []
                        for k in reading_c:
                            sql_script =    ('''SELECT demand_building, id FROM eb_data_clean
                                            WHERE day =? AND season = ? AND time = ?
                                            AND building = ? ORDER BY RANDOM()
                                            LIMIT 1''')
                            sql = cur.execute(sql_script, (sim_startday, sim_season,
                                  timeofday, k))
                            for row in sql:
                                lodem.append(row[0])
                                building_id.append(row[1])

                        total_demand = sum(lodem)/4
                        sql_script = '''INSERT OR IGNORE INTO [data_results]
                                        (load_demand, time, origin1, origin2,
                                        origin3, origin4, building, simulation_id, hour, simulation_num) VALUES (?,?,?,?,?,?, 'building3',?,?,?)'''
                        sql = cur.execute(sql_script, (total_demand,timeofday,
                              building_id[0], building_id[1], building_id[2], building_id[3], sim_id,hour, simulation))

                    elif j == "building4":
                        lodem = []
                        building_id = []
                        for k in reading_c:
                            sql_script =    ('''SELECT demand_building, id FROM eb_data_clean
                                            WHERE day =? AND season = ? AND time = ?
                                            AND building = ? ORDER BY RANDOM()
                                            LIMIT 1''')
                            sql = cur.execute(sql_script, (sim_startday, sim_season,
                                  timeofday, k))
                            for row in sql:
                                lodem.append(row[0])
                                building_id.append(row[1])

                        total_demand = sum(lodem)/4
                        sql_script = '''INSERT OR IGNORE INTO [data_results]
                                        (load_demand, time, origin1, origin2,
                                        origin3, origin4, building, simulation_id, hour, simulation_num) VALUES (?,?,?,?,?,?, 'building4',?,?,?)'''
                        sql = cur.execute(sql_script, (total_demand,timeofday,
                              building_id[0], building_id[1], building_id[2], building_id[3], sim_id, hour, simulation))

                    elif j == "building9":
                        lodem = []
                        building_id = []
                        for k in reading_c:
                            sql_script =    ('''SELECT demand_building, id FROM eb_data_clean
                                            WHERE day =? AND season = ? AND time = ?
                                            AND building = ? ORDER BY RANDOM()
                                            LIMIT 1''')
                            sql = cur.execute(sql_script, (sim_startday, sim_season,
                                  timeofday, k))
                            for row in sql:
                                lodem.append(row[0])
                                building_id.append(row[1])

                        total_demand = sum(lodem)/4
                        sql_script = '''INSERT OR IGNORE INTO [data_results]
                                        (load_demand, time, origin1, origin2,
                                        origin3, origin4, building, simulation_id, hour, simulation_num) VALUES (?,?,?,?,?,?, 'building9',?,?,?)'''
                        sql = cur.execute(sql_script, (total_demand,timeofday,
                              building_id[0], building_id[1], building_id[2], building_id[3], sim_id, hour, simulation))

                    elif j == "building10":
                        lodem = []
                        building_id = []
                        for k in reading_c:
                            sql_script =    ('''SELECT demand_building, id FROM eb_data_clean
                                            WHERE day =? AND season = ? AND time = ?
                                            AND building = ? ORDER BY RANDOM()
                                            LIMIT 1''')
                            sql = cur.execute(sql_script, (sim_startday, sim_season,
                                  timeofday, k))
                            for row in sql:
                                lodem.append(row[0])
                                building_id.append(row[1])

                        total_demand = sum(lodem)/4
                        sql_script = '''INSERT OR IGNORE INTO [data_results]
                                        (load_demand, time, origin1, origin2,
                                        origin3, origin4, building, simulation_id, hour, simulation_num) VALUES (?,?,?,?,?,?, 'building10',?,?,?)'''
                        sql = cur.execute(sql_script, (total_demand,timeofday,
                              building_id[0], building_id[1], building_id[2], building_id[3], sim_id, hour, simulation))

                    elif j == "building12":
                        lodem = []
                        building_id = []
                        for k in reading_c:
                            sql_script =    ('''SELECT demand_building, id FROM eb_data_clean
                                            WHERE day =? AND season = ? AND time = ?
                                            AND building = ? ORDER BY RANDOM()
                                            LIMIT 1''')
                            sql = cur.execute(sql_script, (sim_startday, sim_season,
                                  timeofday, k))
                            for row in sql:
                                lodem.append(row[0])
                                building_id.append(row[1])

                        total_demand = sum(lodem)/4
                        sql_script = '''INSERT OR IGNORE INTO [data_results]
                                        (load_demand, time, origin1, origin2,
                                        origin3, origin4, building, simulation_id, hour, simulation_num) VALUES (?,?,?,?,?,?, 'building12',?,?,?)'''
                        sql = cur.execute(sql_script, (total_demand,timeofday,
                              building_id[0], building_id[1], building_id[2], building_id[3], sim_id, hour, simulation))

                    elif j == "building13":
                        lodem = []
                        building_id = []
                        for k in reading_c:
                            sql_script =    ('''SELECT demand_building, id FROM eb_data_clean
                                            WHERE day =? AND season = ? AND time = ?
                                            AND building = ? ORDER BY RANDOM()
                                            LIMIT 1''')
                            sql = cur.execute(sql_script, (sim_startday, sim_season,
                                  timeofday, k))
                            for row in sql:
                                lodem.append(row[0])
                                building_id.append(row[1])

                        total_demand = sum(lodem)/4
                        sql_script = '''INSERT OR IGNORE INTO [data_results]
                                        (load_demand, time, origin1, origin2,
                                        origin3, origin4, building, simulation_id, hour, simulation_num) VALUES (?,?,?,?,?,?, 'building13',?,?,?)'''
                        sql = cur.execute(sql_script, (total_demand,timeofday,
                              building_id[0], building_id[1], building_id[2], building_id[3], sim_id, hour, simulation))
                    else:
                        lodem = []
                        building_id = []
                        sql_script =    ('''SELECT demand_building, id FROM eb_data_clean
                                        WHERE day =? AND season = ? AND time = ?
                                        AND building = ? ORDER BY RANDOM()
                                        LIMIT 1''')
                        sql = cur.execute(sql_script, (sim_startday, sim_season,
                              timeofday, j))
                        for row in sql:
                            lodem.append(row[0])
                            building_id.append(row[1])

                        total_demand = lodem[0]
                        sql_script = '''INSERT OR IGNORE INTO [data_results]
                                        (load_demand, time, origin1, building, simulation_id, hour, simulation_num) VALUES (?,?,?,?,?,?,?)'''
                        sql = cur.execute(sql_script, (total_demand,timeofday,
                              building_id[0], j, sim_id, hour, simulation))
                date_time = date_time + timedelta(minutes = 60)
                count += 1
                hour += 1
                print count
            print simulation
            simulation += 1


conn.commit()
conn.close()
