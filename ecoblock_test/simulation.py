import numpy as np
import ecoblock_test.get_data as get_data
import matplotlib.pyplot as plt
import time


class System:
    def __init__(self, sim_number, sim_id):
        self.sim_id = sim_id
        self.time_step = 3600
        self.start_date = 1493600340
        self.end_date = 1483311540
        self.simulation_horizon = 24
        self.sim_number = sim_number
        self.load_from_grid = np.zeros((self.simulation_horizon, 1))
        self.load_to_grid = np.zeros((self.simulation_horizon, 1))
        self.ref_price_to_buy = 0.15
        self.ref_price_to_sell = 0.1
        self.flywheel = FlyWheel(self.simulation_horizon, self)

    def set_dates(self, sim_number = 1):
        self.sim_number = sim_number

    def run_simulation(self):
        for i in range(self.simulation_horizon):
            unchanged_consumption = self.load_demand[i] + self.ev_demand[i] - self.pv_generation[i]
            price_to_sell = self.prices_to_sell[i]
            price_to_buy = self.prices_to_buy[i]

            if unchanged_consumption > 0:
                if self.flywheel.is_empty() or price_to_buy <= self.ref_price_to_buy:
                    self.load_from_grid[i] += unchanged_consumption
                else :
                    self.flywheel.discharge(unchanged_consumption, i)
            if unchanged_consumption < 0:
                if self.flywheel.is_full() or price_to_sell >= self.ref_price_to_sell:
                    self.load_to_grid[i] += - unchanged_consumption
                else:
                    self.flywheel.charge(- unchanged_consumption, i)
        self.total_cost = sum(self.load_to_grid)*0.07 + np.dot(self.load_from_grid.T, self.prices_to_buy)

    def load_data(self):
        self.load_demand = get_data.import_load_demand(self.sim_number, self.sim_id)
        self.ev_demand = get_data.import_ev_demand(self.sim_number, self.sim_id)
        self.pv_generation = get_data.import_pv_generation(self.sim_number, self.sim_id)
        self.prices_to_sell = get_data.import_prices_to_sell(self.simulation_horizon)
        self.prices_to_buy = get_data.import_prices_to_buy(self.simulation_horizon)

    def plot_results(self):
        dates = [self.start_date + 3600*i for i in range(self.simulation_horizon)]
        labels = [time.strftime('%H:%M:%S', time.gmtime(date)) for date in dates]
        to_plot = [(self.load_from_grid, 'load from grid'),
                (self.load_to_grid, 'load to grid'),
                (self.flywheel.soc_record, 'flywheel load'),
                (self.load_demand, 'load demand'),
                (self.ev_demand, 'ev demand'),
                (self.pv_generation, 'pv generation'),
                ([1000*price for price in self.prices_to_buy], 'prices to buy')]
        plt.figure(figsize=(20, 10))
        for i in range(len(to_plot)):
            plt.plot(dates, to_plot[i][0], label=to_plot[i][1])
            plt.xticks(dates, labels, rotation='vertical')
            plt.tick_params(labelsize=6)
            plt.xlabel('time')
        plt.grid()
        plt.legend()
        plt.savefig('result.png')

    def get_cost(self):
        return self.total_cost


class FlyWheel:
    def __init__(self, simulation_horizon, system):
        self.soc_record = np.zeros((simulation_horizon, 1))
        self.capacity = 480
        self.charging_rate_max_in_hour = 120
        self.discharging_rate_max_in_hour = 120
        self.system = system

    def is_full(self):
        return sum(self.soc_record) >= self.capacity

    def is_empty(self):
        return sum(self.soc_record) <= 0

    def charge(self, energy, index):
        if not self.is_full():
            if (self.capacity - sum(self.soc_record)) >= energy:
                if self.charging_rate_max_in_hour >= energy:
                    self.soc_record[index] += energy
                else:
                    self.soc_record[index] += self.charging_rate_max_in_hour
                    self.system.load_to_grid[index] += energy - self.charging_rate_max_in_hour
            else:
                energy_enabled = self.capacity - sum(self.soc_record)
                if self.charging_rate_max_in_hour >= energy_enabled:
                    self.soc_record[index] += energy_enabled
                else:
                    self.soc_record[index] += self.charging_rate_max_in_hour
                    self.system.load_to_grid[index] += energy_enabled - self.charging_rate_max_in_hour
                self.system.load_to_grid[index] += energy - energy_enabled

    def discharge(self, energy, index): #energy needs to be > 0
        if not self.is_empty():
            if sum(self.soc_record) >= energy:
                if self.discharging_rate_max_in_hour >= energy:
                    self.soc_record[index] += - energy
                else:
                    self.soc_record[index] += self.discharging_rate_max_in_hour
                    self.system.load_from_grid[index] += energy - self.discharging_rate_max_in_hour
            else:
                energy_enabled = sum(self.soc_record)
                if self.discharging_rate_max_in_hour >= energy_enabled:
                    self.soc_record[index] += - energy_enabled
                else:
                    self.soc_record[index] += self.discharging_rate_max_in_hour
                    self.system.load_from_grid[index] += - energy_enabled + self.discharging_rate_max_in_hour
                self.system.load_from_grid[index] += - energy + energy_enabled
