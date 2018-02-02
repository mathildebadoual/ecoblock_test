import sqlite3
import datetime
from datetime import datetime
import time
import os
import csv
import re



conn = sqlite3.connect('astrodek.sqlite')
cur = conn.cursor()


reading_a = []
reading_b = []

sql_script = ('SELECT date, day, season, building FROM eb_data_raw')
sql = cur.execute(sql_script)

for row in sql:
    reading_a.append(row)

for row in reading_a:
    date = row[0]
    date_time = (datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))
    timeofday = str(date_time.time())
    sql_script = 'INSERT OR IGNORE INTO eb_data_clean (building, day, date_time, season, time) VALUES (?,?,?,?,?)'
    cur.execute (sql_script, (row[3], row[1], date_time, row[2], timeofday))
conn.commit()
conn.close()
