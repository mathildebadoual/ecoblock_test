import numpy as np
import get_data as get_data
import random


# irradiance in 1 kW/m**2 = 1 sun

def pv_generation(irradiance):
    open_circuit_voltage = 0.612
    temperature = 25
    coeff = 0.0257
    return coeff * (open_circuit_voltage + np.log(irradiance))



class IndividualHome:
    def __init__(self, start_date, end_date):
        self.storage_battery_soc = []
        self.ev_battery_soc = []
        self.start_date = start_date
        self.end_date = end_date


    def battery_charged(self, energy_stored):
        self.storage_battery_soc += energy_stored

    def ev_charging(self, energy_charging):
        if self.car_is_here:
            self.ev_battery_soc += energy_charging

    def car_is_here(self):
        #to improve with the distribution from data
        return random.randint(0, 1)

    def set_solar_generatioin(self):
        self.solar_generation = get_data.load_pv_irradiance(self.start_date, self.end_date)[0]
        # create dictionnary for the date->key and solar_gen->values

    def get_solar_generation(self, date):
        return self.solar_generation[date]

    def set_consummer_load(self):
        self.consummer_load = get_data.load_pv_irradiance(self.start_date, self.end_date)[0]
        # create dictionnary for the date->key and solar_gen->values

    def get_consummer_load(self, date):
        return self.consummer_load[date]








class System:
    def __init__(self, start_time, end_time):
        # add function to have a finite number of interval of size decided (here 15 min)
        self.start_time = start_time
        self.end_time = end_time
        self.solar_consumption = []
        self.

    def generate_houses(self):
        pass

    def run_simulation(self):
        pass

    def run_step(self):
        pass

    def next_step(self):
        pass

    def plot_results(self):
        pass

