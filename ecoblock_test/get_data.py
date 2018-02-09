import sqlite3
import numpy as np
import pandas as pd

DATA_PATH = '/Users/mathildebadoual/code/ecoblock_test/data/database.sqlite'

def import_load_demand(sim_number, sim_id):
    conn = sqlite3.connect(DATA_PATH)
    cur = conn.cursor()
    sql_script = ('SELECT demand FROM results WHERE simulation_id = ? AND simulation_num = ?')
    cur.execute(sql_script, (str(sim_id), str(sim_number)))
    load_demand = cur.fetchall()
    conn.close()
    return np.array(load_demand)

def import_ev_demand(sim_number, sim_id):
    conn = sqlite3.connect(DATA_PATH)
    cur = conn.cursor()
    sql_script = ('SELECT ev_demand FROM results WHERE simulation_id = ? AND simulation_num = ?')
    cur.execute(sql_script, (str(sim_id), str(sim_number)))
    ev_demand = cur.fetchall()
    conn.close()
    return np.array(ev_demand)

def import_pv_generation(sim_number, sim_id):
    conn = sqlite3.connect(DATA_PATH)
    cur = conn.cursor()
    sql_script = ('SELECT pv_generation FROM results WHERE simulation_id = ? AND simulation_num = ?')
    cur.execute(sql_script, (str(sim_id), str(sim_number)))
    pv_generation = cur.fetchall()
    conn.close()
    return np.array(pv_generation)

def import_prices_to_buy(simulation_horizon):
    data = pd.read_csv('/Users/mathildebadoual/code/ecoblock_test/data/prices_a10.csv')
    prices_to_buy = data['prices_to_buy_summer'].as_matrix()
    return prices_to_buy

def import_prices_to_sell(simulation_horizon):
    return np.array([0.07] * int(simulation_horizon))
