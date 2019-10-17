import ciw
import pandas as pd
import matplotlib.pyplot as plt
import os

assert ciw.__version__ == '1.1.5', "ciw package is not the correct version (1.1.5) to run this function!" 

user_name = os.getcwd().split('\\')[2].split('.')[0].capitalize()
print(f'\nOlá, {user_name}!')

class Simulation:


    def __init__(self, number_of_servers,
                          arrivals_per_hour,
                          service_mins_per_server,
                          #warm_up_time,
                          max_hrs_time,
                          arrival_distribution='Exponential'):

        self.number_of_servers = number_of_servers
        self.arrivals_per_hour = arrivals_per_hour
        self.service_mins_per_server = service_mins_per_server
        # self.warm_up_time = warm_up_time
        self.max_hrs_time = max_hrs_time
        self.arrival_distribution = arrival_distribution
                

    # # time_dependent_batches function
    # # cria blocos de chegadas em função de tempos de chegada (t unidades de tempo)

    # def time_dependent_batches(self, t):

    #     self.t = t

    #     assert t > 0, "Value of t needs to be bigger than zero!"

    #     if t < 2.0:
    #         return 100 # primeiras t horas: x chegadas
    # #     if t < 3.0:
    # #         return 50
    #     return 1



    # simulation function

    def simulate_waiting_time(self):

        '''
        parameters:
        
            number_of_servers: nr of counters/desks
            arrivals_per_hour: nr of arrivals per hour (mean)
            service_mins_per_server: amount of time (in mins) a customer spends with a server (mean)
            max_time: hours to simulate for
            ####warm_up_time: warm-up time of 50 time units (from arrival date)
            arrival_distribution: setting arrivals according to a probability distribution
            
            
        returns:
            
            Q : simulation object, resulting in several attributes per node, such as waiting times and queue sizes
            
        '''

        number_of_servers = self.number_of_servers
        arrivals_per_hour = self.arrivals_per_hour
        service_mins_per_server = self.service_mins_per_server
        # warm_up_time = self.warm_up_time
        max_hrs_time = self.max_hrs_time
        arrival_distribution = self.arrival_distribution

        
        assert number_of_servers > 0, "Number of servers needs to be bigger than zero!"

        max_time = max_hrs_time * 60
        lamda = arrivals_per_hour / 60 # our λ
        mue = 1 / service_mins_per_server # our μ
        
        # This is the distribution that inter-arrival times are drawn from;
        # that is, the time between two consecutive arrivals
        
        if arrival_distribution == 'Weibull':
            arrival_distributions = ['Weibull', 1, 1]
        elif arrival_distribution == 'Gamma':
            arrival_distributions = ['Gamma', 1, 1]
        else:
            arrival_distributions = ['Exponential', lamda]
        
        service_distributions = ['Exponential', mue] # amount of time a customer spends with a server
        
        N = ciw.create_network(
        
            # distribution of times between arrivals; here, 12 per hour would mean an average of 5 mins between arrivals (12 / 60 segs)
            #Arrival_distributions=[['Exponential', 6.0], ['Exponential', 2.5]],
            Arrival_distributions=[arrival_distributions],

            # nr mesas
            #Number_of_servers=[1, 1], 
            Number_of_servers=[number_of_servers], # [1, 1], 

            # capacidade total de fila (nr cidadaos na fila)
            #Queue_capacities=['Inf', 4],
            
    #         Batching_distributions=[['Deterministic', 2]],
            
            # Batching_distributions=[['TimeDependent', time_dependent_batches]],
            
            # distribution of times spent in service with a server (mean), i.e amount of time a customer spends with a server
            #Service_distributions=[['Exponential', 8.5], ['Exponential', 5.5]],
            Service_distributions=[service_distributions]

            #, Transition_matrices=[[0.0, 0.2], [0.1, 0.0]]
        
        )
        
    #     ciw.seed(0)
    #     Q = ciw.Simulation(N)
        
    #     Q.simulate_until_max_time(max_time, progress_bar=True)
    #     server_busy_time = Q.transitive_nodes
    #     recs = Q.get_all_records()
    #     waits = [r.waiting_time for r in recs]

        # over n trials
        
        trials = 100

        # average_waits = []
        for trial in range(trials):
            ciw.seed(trial)
            Q = ciw.Simulation(N)
    #         Q.simulate_until_max_customers(300*11, method='Finish')
            Q.simulate_until_max_time(max_time)
    #         server_busy_time = Q.transitive_nodes
    #         recs = Q.get_all_records()
    #         waits = [r.waiting_time for r in recs]
            
        return Q #, server_busy_time, waits, recs
