import sqlite3

conn = sqlite3.connect('/Users/mathildebadoual/code/ecoblock_test/data/load_demand/astrodek.sqlite')
cur = conn.cursor()

sql_script = ('SELECT date, day, season, building FROM eb_data_raw')
sql = cur.execute(sql_script)
