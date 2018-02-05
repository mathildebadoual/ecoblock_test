import numpy as np
import get_data as get_data
import random
import ecoblock_test.get_data as get_data
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

# irradiance in 1 kW/m**2 = 1 sun

def pv_generation(irradiance):
    open_circuit_voltage = 0.612
    temperature = 25
    coeff = 0.0257
    return coeff * (open_circuit_voltage + np.log(irradiance))


class System:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.time_step = 3600
        slef.simulation_horizon = (self.end_time - self.start_time) / self.time_step
        self.load_from_grid = [0]*self.simulation_horizon
        self.load_to_grid = [0]*self.simulation_horizon
        self.ref_price_to_buy = 10
        self.ref_price_to_sell = 10
        self.flywheel = FlyWheel(self.simulation_horizon, self)

    def run_simulation(self):
        for i in range(self.simulation_horizon):
            unchanged_consumption = self.load_demand[i] + self.ev_demand[i] - selfpv_generation[i]
            price_to_sell = self.prices_to_sell[i]
            price_to_buy = self.prices_to_buy[i]
            if unchanged_consumption < 0:
                if self.flywheel.is_empty() or price_to_buy <= self.ref_price_to_buy:
                    self.load_from_grid[i] += unchanged_consumption
                else :
                    self.flywheel.discharge(unchanged_consumption, i)
            if unchanged_consumption > 0:
                if self.flywheel.is_full() or price_to_sell >= self.ref_price_to_sell:
                    self.load_to_grid[i] += unchanged_consumption
                else:
                    self.flywheel.charge(unchanged_consumption, i)

    def load_data(self):
        self.load_demand = get_data.import_load_demand(self.start_date, self.end_date)
        self.ev_demand = get_data.import_ev_demand(self.start_date, self.end_date)
        self.pv_generation = get_data.import_pv_generation(self.start_date, self.end_date)
        self.prices_to_sell = get_data.import_prices_to_sell(self.start_date, self.end_date)
        self.prices_to_buy = get_data.import_prices_to_buy(self.start_date, self.end_date)

    def plot_results(self):
        dates = [self.start_date + 3600*i for i in range(self.simulation_horizon)]
        dates = mdate.epo2num(dates)
        date_fmt = '%d-%m-%y %H:%M:%S'
        date_formatter = mdate.DateFormatter(date_fmt)

        to_plot = [(self.load_from_grid, 'load from grid'), (0.07*self.load_to_grid, 'load to grid'), (self.flywheels.soc_record, 'flywheel load'),
                (self.load_demand, 'load demand'), (self.ev_demand, 'ev demand'), (self.pv_generation, 'pv generation')]
        plt.figure(figsize=(10, 5))

        for i in range(len(to_plot)):
            fig, ax = plt.subplot(611+i)
            ax.plot_date(dates, to_plot[i][0])
            ax.xaxis.set_major_formatter(date_formater)
            plt.title(to_plot[i][0])
            plt.xlabel('time')
        plt.show()


class FlyWheel:
    def __init__(self, simulation_horizon, system):
        self.soc_record = [0]*simulation_horizon
        self.capacity = 480
        self.charging_rate_max_in_hour = 120
        self.discharging_rate_max_in_hour = - 120
        self.system = system

    def is_full(self):
        return sum(self.soc_record) == self.capacity

    def is_empty(self):
        return sum(self.soc_record) == 0

    def charge(self, energy, index):
        if not self.is_not_full():
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
        if not self.is_not_empty():
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



