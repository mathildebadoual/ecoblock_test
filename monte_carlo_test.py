import numpy as np
import get_data as get_data


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

    def run_simulation(self):
        pass

    def run_step(self):
        pass

    def next_step(self):
        pass

    def plot_results(self):
        pass

