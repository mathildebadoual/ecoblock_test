import ecoblock_test.monte_carlo_test as mct

start_date = 1483232340
end_date = 1483487940
system = mct.System(start_date, end_date)

system.load_data()
system.run_simulation()
system.plot_results()
