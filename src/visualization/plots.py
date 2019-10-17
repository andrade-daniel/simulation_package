
import matplotlib.pyplot as plt
import os

current_folder = os.path.dirname(os.path.abspath(__file__))

output_folder = current_folder + r'\output'
file_path = r'\waiting_times_mean.png'

def plot_waiting_mean(waits, average_waits, number_of_servers, arrivals_per_hour, service_mins_per_server):
    # average_waits = sum(waits) / len(waits)
    plt.hist(waits)
    plt.axvline(x=average_waits, linewidth=3, c='r')
    plt.xlabel(f'mean waiting time: {round(average_waits, 2)} mins') 
    plt.title(f'Mean waiting time (mins): {round(average_waits, 2)} \nNumber of servers: {number_of_servers} \nArrivals per hour: {arrivals_per_hour} \nService time (mins): {service_mins_per_server}')

    plt.savefig(output_folder + file_path, bbox_inches='tight')
    plt.show()
