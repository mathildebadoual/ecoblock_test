import sqlite3

conn = sqlite3.connect('/Users/mathildebadoual/code/ecoblock_test/data/load_demand/astrodek.sqlite')
cur = conn.cursor()


def import_load_demand(start_date, end_date):
    sql_script = ('SELECT  demand FROM results WHERE timestamp>= start_date AND timestamp <= end_date')
    sql = cur.execute(sql_script)
    return cur.fetchall()

def import_ev_demand(strat_date, end_date):
    sql_script = ('SELECT ev_demand FROM results WHERE timestamp >=start_date ADN timestamp <= end_date')
    sql = cur.execulte(sql_script)

start_date = 1493600340
end_date = 1493683140
print(import_load_demand(start_date, end_date))
conn.close()

