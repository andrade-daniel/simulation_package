from src.run_sim.sim_function import Simulation
from src.visualization.plots import *
import argparse


# parser argument definition

parser = argparse.ArgumentParser()

parser.add_argument("-servers", "--number_of_servers", help = "Number of servers/desks", required = False,
default = 1)

parser.add_argument("-arrivals", "--arrivals_per_hour", help = "Citizens arriving per hour", required = True)

parser.add_argument("-service", "--service_mins_per_server", help = "Average service in minutes", required = True)

parser.add_argument("-max_time", "--max_hrs_time", help = "Maximum hours for simulation run", required = False,
default=14)

args = parser.parse_args()

print("\nYou have set the following parameters: \nnumber_of_servers: {} \narrivals_per_hour: {} \nservice_mins_per_server: {} \nmax_hrs_time: {}".format(
        args.number_of_servers,
        args.arrivals_per_hour,
        args.service_mins_per_server,
        args.max_hrs_time
        ))

number_of_servers = int(args.number_of_servers)
arrivals_per_hour = int(args.arrivals_per_hour)
service_mins_per_server = int(args.service_mins_per_server)
# warm_up_time = int(args.warm_up_time)
max_hrs_time = int(args.max_hrs_time)

# set parameters dictionary

params = {'number_of_servers': number_of_servers,
          'arrivals_per_hour': arrivals_per_hour,
          'service_mins_per_server': service_mins_per_server,
          #'warm_up_time': warm_up_time,
          'max_hrs_time': max_hrs_time}

# instantiate

sim = Simulation(**params)

# run simulation!

Q = sim.simulate_waiting_time()

# extract results

server_busy_time = Q.transitive_nodes
recs = Q.get_all_records()

if sim.number_of_servers > 1:
    warm_up_time = 60
else:
    warm_up_time = 0

recs = [r for r in recs if r.arrival_date > warm_up_time]

waits = [r.waiting_time for r in recs]
average_waits = sum(waits) / len(waits)

print(f'Mean waiting time (mins): {round(average_waits, 2)} \nNumber of servers: {sim.number_of_servers} \nArrivals per hour: {sim.arrivals_per_hour} \nService time (mins): {sim.service_mins_per_server}')
print([(f'Service/Node {idx} is busy {round(k.server_utilisation*100, 2)}% of the time') for idx, k in enumerate(server_busy_time)][0])

# to plot

plot_params = {k: params[k] for k in params.keys() if k != 'max_hrs_time'}

plot_waiting_mean(waits, average_waits, **plot_params)

