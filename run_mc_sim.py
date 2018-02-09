import ecoblock_test.simulation as sim
import matplotlib.pyplot as plt
import pandas as pd


NUMBER_OF_SIMULATIONS = 20
NUMBER_OF_SIMULATIONS_ID = 28

cost_record = []

def plot_hist(data):
    num_bins = 30
    data.hist(bins=num_bins)
    plt.xlabel('Cost in $/day')
    plt.ylabel('Distribution')
    plt.grid(True)
    plt.savefig('hist_cost.png')

for sim_id in range(1, NUMBER_OF_SIMULATIONS_ID + 1):
    for sim_number in range(1, NUMBER_OF_SIMULATIONS + 1):
        print('sim_id:', sim_id, 'and sim_number:', sim_number)
        system = sim.System(sim_number, sim_id)
        system.load_data()
        system.run_simulation()
        cost_record.append(system.get_cost())

cost_record_df = pd.DataFrame(cost_record, columns=['cost'])
plot_hist(cost_record_df['cost'])
