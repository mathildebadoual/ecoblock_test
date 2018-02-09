import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import sqlite3
from datetime import datetime
from matplotlib.dates import DateFormatter, HourLocator, MinuteLocator

fs = 8
conn = sqlite3.connect('astrodek.sqlite')
cur = conn.cursor()

sql_script =    ('''SELECT time, demand, ev_demand  FROM results WHERE simulation_id = 1 and simulation_num = 1 ORDER BY id DESC''')
sql = cur.execute(sql_script)

x_values = []
y_values_houses = []
y_values_ev = []

for row in sql:
    sim_hour = row[0]
    date_time = (datetime.strptime(sim_hour, '%H:%M:%S'))
    x_values.append(date_time)
    y_values_houses.append(row[1])
    y_values_ev.append(row[2])

date_list = matplotlib.dates.date2num(x_values)
fig, axes_array = plt.subplots(3, sharex=True, figsize=(9, 7))

axes_array[0].plot(date_list,y_values_houses,label="Houses")
axes_array[0].set_ylabel("kWh", fontsize=fs)
axes_array[0].tick_params(axis='both', which='major', labelsize=fs)
axes_array[0].set_ylim([5,100])
axes_array[0].set_yticks(np.arange(0,100,20))
axes_array[0].legend(fontsize=fs)

axes_array[1].plot(date_list, y_values_ev, label="EV")
axes_array[1].set_ylabel("kWh", fontsize=fs)
axes_array[1].tick_params(axis='both', which='major', labelsize=fs)
axes_array[1].set_ylim([0,50])
axes_array[1].set_yticks(np.arange(0,50,10))
axes_array[1].legend(fontsize=fs)

axes_array[1].xaxis.set_major_locator( MinuteLocator(np.arange(0,60,60)) )
axes_array[1].xaxis.set_major_formatter( DateFormatter('%H') )
axes_array[1].fmt_xdata = DateFormatter('%H')

plt.tight_layout()
plt.subplots_adjust(bottom=0.1,top=0.98, hspace=0.02)

plt.show()
