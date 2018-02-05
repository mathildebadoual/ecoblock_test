import sqlite3

conn = sqlite3.connect('/Users/mathildebadoual/code/ecoblock_test/data/load_demand/astrodek.sqlite')
cur = conn.cursor()


def import_load_demand(start_date, end_date):
    sql_script = ('SELECT  demand FROM results WHERE time >= start_date AND time <= end_date')
    sql = cur.execute(sql_script)
    return cur.fetchall()

def import_ev_demand(strat_date, end_date):
    sql_script = ('SELECT ev_demand FROM results WHERE time >=start_date ADN tine <= end_date')
    sql = cur.execulte(sql_script)


print(import_load_demand(
conn.close()

