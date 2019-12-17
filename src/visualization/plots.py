
import numpy as np
import matplotlib.pyplot as plt
import os

current_folder = os.path.dirname(os.path.abspath(__file__))

output_folder = current_folder + r'\output'
file_path = r'\waiting_times_mean.png'

# def plot_waiting_mean(waits, average_waits, mean_service_time, number_of_servers, arrivals_per_hour):
def plot_waiting_mean(waits, average_waits):
    # average_waits = sum(waits) / len(waits)
    plt.hist(waits)
    plt.axvline(x=average_waits, linewidth=3, c='r')
    # plt.xlabel(f'\nMean waiting time: {round(average_waits, 2)} mins \nWaiting max: {round(np.max(waits), 2)}') 
    # plt.title(f'Simulated service time (mins): {round(mean_service_time, 2)} \nMean waiting time: {round(average_waits, 2)} mins \nWaiting max: {round(np.max(waits), 2)}')
    # plt.title(f'Tempo médio de espera: {round(average_waits, 2)} mins \nTempo máximo de espera: {round(np.max(waits), 2)} mins')

    plt.savefig(output_folder + file_path, bbox_inches='tight')
    plt.show()
