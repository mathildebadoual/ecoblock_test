#!/bin/bash
python results_data.py &
wait
python ev_results.py &
wait
python results.py &
wait
python graph_results.py &
