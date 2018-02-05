The objective of the load_demand program is create an aggregate load demand
scenario for short periods of time given different load readings.  It is
specifically design to generate random load demand for a specific grid given
access to some of the load demand readings from the units in the grid. The
program uses the following inputs:
i)	start_day (day of the week in number, i.e. Monday = 0, Tuesday = 1 …)
ii)	start_time (hh:mm:ss)
iii)	hours (total hours to be simulated)
iv)	simulations (number of simulations)
v)	season (fall, spring)

Given this inputs, the program selects a load_demand that satisfies all the
criteria for each of the buildings in the block. It then aggregates the load
per hour to give the aggregate load of the grid.
The program takes into account the likely scenario that not all the data load
demand from the grid will be available and thus some buildings/apartments will
need to be estimated. To overcome this, the readings that are available are
used to estimate the load of those buildings/apartments with similar
characteristics.
If running the program for the first time or adding new data to the program
follows the steps from 1. Since the program needs to order large number of data
points and if the database has already been created, it is recommended to only
run steps 7 and 8 to generate the load demand scenarios OR (if no new data will be added to the database) just do step 7 and run run_simulation.bs
The steps to run the program from the beginning are:
1.	Store the csv load demand readings in the DATA folder.
2.	Fill the main_data_eb.csv file in the DATA folder
3.	Run structuredatabase.py will create the structure of the database
4.	Run raw_buildingmeasured.py reads all the input files (.csv files) and populates the eb_data_raw table in the astrodek.sqlite database.
5.	Run clean_buildingmeasured.py to create unique building, season, day and daytime entries
6.	Run building_aggregate_load.py  populates the load of each unique building, season, day and daytime entries
7.	Fill the results.csv file in the DATA folder to give the parameters to the
    simulation
8.	Run building_event_data.py to populates the results_data table in the
    astrodek.sqlite database. This table is mainly created to have traceability
    to the origin of the data used on the simulation
9.	Run raw_evmeasured.py reads all the input files (.csv files) for the ev use and populates the ev_raw table
10.	Run ev_event_data.py to populates the ev_state table in the
    astrodek.sqlite database. This table is mainly created to have traceability
    to the origin of the data used on the simulation
11.	Run event_results.py to generate the aggregate building load scenario and aggregate ev load demand scenarios
