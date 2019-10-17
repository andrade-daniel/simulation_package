# to run all tests:
# >  pytest 
# to run this test:
# >  pytest .\tests\run_sim\test_sim_function.py

import pytest
# from simulation_package.src.run_sim.sim_function import time_dependent_batches, simulate_waiting_time
from simulation_package.src.run_sim.sim_function import Simulation

# class TestTimeDependentBatches(object):

#     def test_time_dependent_batches(self):
        
#         # to guarantee t > 0
#         t = 0

#         # Store information about raised AssertionError in exc_info
#         expected_error_msg = "Value of t needs to be bigger than zero!"
#         with pytest.raises(AssertionError) as exc_info:
#             time_dependent_batches(t)

#         # Check if the raised ValueError contains the correct message
#         assert exc_info.match(expected_error_msg)


class TestSimulateWaitingTime(object):

    def test_simulation_function_nr_servers(self):
        
        # to guarantee nr servers > 0
        test_nr_servers = 0

        arrivals_per_hour = 1
        service_mins_per_server = 1
        #warm_up_time,
        max_hrs_time = 1
        arrival_distribution = 'Exponential'

        # Store information about raised AssertionError in exc_info
        expected_error_msg = "Number of servers needs to be bigger than zero!"
        with pytest.raises(AssertionError) as exc_info:
            # simulate_waiting_time(test_nr_servers, arrivals_per_hour, service_mins_per_server, max_hrs_time, arrival_distribution)
            sim = Simulation(test_nr_servers, arrivals_per_hour, service_mins_per_server, max_hrs_time, arrival_distribution)    
            sim.simulate_waiting_time()
            
        # Check if the raised ValueError contains the correct message
        assert exc_info.match(expected_error_msg)



