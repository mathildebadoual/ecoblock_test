import numpy as np
import get_data as get_data


# irradiance in 1 kW/m**2 = 1 sun

def pv_generation(irradiance):
    open_circuit_voltage = 0.612
    temperature = 25
    coeff = 0.0257
    return coeff * (open_circuit_voltage + np.log(irradiance))


def
