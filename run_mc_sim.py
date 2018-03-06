import ecoblock_test.simulation as sim
import matplotlib.pyplot as plt
import pandas as pd


NUMBER_OF_SIMULATIONS = 20
NUMBER_OF_SIMULATIONS_ID = 28

cost_record = []

def plot_hist(data):
    plt.figure()
    num_bins = 30
    data.hist(bins=num_bins)
    plt.xlabel('Cost in $/day')
    plt.ylabel('Simulation results')
    plt.grid(True)
    plt.savefig('hist_cost.png')

sim_id_list = []
sim_number_list = []

for sim_id in range(1, NUMBER_OF_SIMULATIONS_ID + 1):
    for sim_number in range(1, NUMBER_OF_SIMULATIONS + 1):
        print('sim_id:', sim_id, 'and sim_number:', sim_number)
        sim_id_list.append(sim_id)
        sim_number_list.append(sim_number)
        system = sim.System(sim_number, sim_id)
        system.load_data()
        system.run_simulation()
        cost_record.append(system.get_cost())

        #print('Is at cost:', system.get_cost())
        #system.plot_results()
        #file_name = 'normal' + str(sim_number) + '-' + str(sim_id) + '.png'
        #plt.savefig(file_name)

data_result = pd.DataFrame(sim_id_list, columns=['sim_id'])
data_result['sim_num'] = sim_number_list
data_result['cost'] = cost_record
data_result.to_csv('data_result.csv')
cost_record_df = pd.DataFrame(cost_record, columns=['cost'])
plot_hist(cost_record_df['cost'])
