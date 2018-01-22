import sqlite3
import datetime
from datetime import datetime
import time
import os
import csv
import re

ecoblock = {'building1':2, 'building2':2, 'building3':3, 'building4':2,
            'building5':3, 'building6':2, 'building7':12, 'building8':8,
            'building9':2, 'building10':2, 'building11':2, 'building12':2,
            'building13':3, 'house':20}


conn = sqlite3.connect('astrodek.sqlite')
cur = conn.cursor()


reading_a = []
reading_b = []


sql_script = ('SELECT building, date_time FROM eb_data_clean')
sql = cur.execute(sql_script)

for row in sql:
    reading_a.append(row)
count = 0
for row in reading_a:
    parameter1 = str(row[0])
    parameter2 = str(row[1])

    #Compute the sum of the readings that satisfy a condition
    sql_script = 'SELECT SUM (load_demand) FROM eb_data_raw WHERE building = ? AND date = ?'
    load_sum = cur.execute(sql_script,(parameter1,parameter2))
    for i in load_sum:
        load = float(i[0])
        sql_script = 'UPDATE eb_data_clean SET total_demand = ? WHERE building = ? AND date_time = ?'
        sql = cur.execute(sql_script,(load, parameter1, parameter2))

    #Compute the count of the readins that satisy a condition
    sql_script = 'SELECT COUNT (*) FROM eb_data_raw WHERE building = ? AND date = ?'
    load_count = cur.execute(sql_script, (parameter1,parameter2))
    for i in load_count:
        count = float(i[0])
        sql_script = 'UPDATE eb_data_clean SET readings = ? WHERE building = ? AND date_time = ?'
        sql = cur.execute(sql_script,(count, parameter1, parameter2))

    #Compute the average demand of the readings satisfying the condition
    sql_script = 'SELECT AVG (load_demand) FROM eb_data_raw WHERE building = ? AND date = ?'
    load_avg = cur.execute(sql_script, (parameter1,parameter2))
    for i in load_avg:
        average = float(i[0])
        building = average * ecoblock[parameter1]
        sql_script = 'UPDATE eb_data_clean SET apt_average = ?, demand_building = ? WHERE building = ? AND date_time = ?'
        sql = cur.execute(sql_script,(average, building, parameter1, parameter2))


conn.commit()
conn.close()
