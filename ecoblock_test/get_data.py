import sqlite3
import numpy as np
import pandas as pd


DATA_PATH = '/Users/mathildebadoual/code/ecoblock_test/data/load_demand/astrodek.sqlite'

def import_load_demand(start_date, end_date):
    conn = sqlite3.connect(DATA_PATH)
    cur = conn.cursor()
    sql_script = ('SELECT demand FROM results WHERE timestamp >= ? AND timestamp <= ? ')
    cur.execute(sql_script, (start_date, end_date))
    load_demand = cur.fetchall()
    conn.close()
    return np.array(load_demand)

def import_ev_demand(start_date, end_date):
    conn = sqlite3.connect(DATA_PATH)
    cur = conn.cursor()
    sql_script = ('SELECT ev_demand FROM results WHERE timestamp >= ? AND timestamp <= ? ')
    cur.execute(sql_script, (start_date, end_date))
    ev_demand = cur.fetchall()
    conn.close()
    return np.array(ev_demand)

def import_pv_generation(start_date, end_date):
    data = pd.read_csv('/Users/mathildebadoual/code/ecoblock_test/data/pv_generation.csv')
    pv_generation = data['pv_generation'].as_matrix()
    return pv_generation

def import_prices_to_buy(start_date, end_date):
    data = pd.read_csv('/Users/mathildebadoual/code/ecoblock_test/data/prices_a10.csv')
    prices_to_buy_day = data['prices_to_buy_summer'].as_matrix()
    simulation_horizon = (end_date - start_date) / 3600
    prices_to_buy = prices_to_buy_day
    for i in range(int(simulation_horizon / 24)):
        prices_to_buy = np.concatenate((prices_to_buy, prices_to_buy_day))
    return prices_to_buy


def import_prices_to_sell(start_date, end_date):
    simulation_horizon = (end_date - start_date) / 3600
    return np.array([0.07] * int(simulation_horizon + 1))
