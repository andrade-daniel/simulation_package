# to run test first time:
# >  pytest -k "test_plot_waiting_mean" --mpl-generate-path visualization/baseline
# to run test after first time:
# >  pytest -k "test_plot_waiting_mean" --mpl

import pytest
from simulation_package.src.visualization.plots import plot_waiting_mean
import numpy as np

def test_plot_waiting_mean():

    waits = np.random.normal(100, 20, size=100)
    average_waits = 100
    number_of_servers = 20
    arrivals_per_hour = 100
    service_mins_per_server = 10
    
    return plot_waiting_mean(waits, average_waits, number_of_servers, arrivals_per_hour, service_mins_per_server)



