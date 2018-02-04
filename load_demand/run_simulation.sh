#!/bin/bash
python building_event_data.py &
wait
python ev_event_data.py &
wait
python event_results.py &
wait
python graph_results.py &
